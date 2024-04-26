from ninja_extra import api_controller, ControllerBase, route
from ninja import Query
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated
from ninja.pagination import paginate
from utils.chen_pagination import MyPagination
from django.db import transaction
from django.shortcuts import get_object_or_404
from typing import List
from utils.chen_response import ChenResponse
from utils.chen_crud import multi_delete_testDemand
from apps.project.models import Design, Dut, Round, TestDemand, TestDemandContent
from apps.project.schemas.testDemand import DeleteSchema, TestDemandModelOutSchema, TestDemandFilterSchema, \
    TestDemandTreeReturnSchema, TestDemandTreeInputSchema, TestDemandCreateOutSchema, TestDemandCreateInputSchema, \
    TestDemandRelatedSchema, TestDemandExistRelatedSchema
# 导入ORM
from apps.project.models import Project

@api_controller("/project", auth=JWTAuth(), permissions=[IsAuthenticated], tags=['测试项接口'])
class TestDemandController(ControllerBase):
    @route.get("/getTestDemandList", response=List[TestDemandModelOutSchema], exclude_none=True,
               url_name="testDemand-list")
    @transaction.atomic
    @paginate(MyPagination)
    def get_test_demand_list(self, datafilter: TestDemandFilterSchema = Query(...)):
        for attr, value in datafilter.__dict__.items():
            if getattr(datafilter, attr) is None:
                setattr(datafilter, attr, '')
        design_key = "".join([datafilter.round_id, '-', datafilter.dut_id, '-', datafilter.design_id])
        qs = TestDemand.objects.filter(project__id=datafilter.project_id, design__key=design_key,
                                       ident__icontains=datafilter.ident,
                                       name__icontains=datafilter.name,
                                       testType__contains=datafilter.testType,
                                       priority__icontains=datafilter.priority).order_by("key")
        # 由于有嵌套query_set存在，把每个测试需求的schema加上一个字段
        query_list = []
        for query_single in qs:
            setattr(query_single, "testContent", query_single.testQField.all().values())
            query_list.append(query_single)
        return query_list

    # 处理树状数据
    @route.get("/getTestdemandInfo", response=List[TestDemandTreeReturnSchema], url_name="testDemand-info")
    @transaction.atomic
    def get_testDemand_tree(self, payload: TestDemandTreeInputSchema = Query(...)):
        qs = TestDemand.objects.filter(project__id=payload.project_id, design__key=payload.key)
        return qs

    # 添加测试项
    @route.post("/testDemand/save", response=TestDemandCreateOutSchema, url_name="testDemand-create")
    @transaction.atomic
    def create_test_demand(self, payload: TestDemandCreateInputSchema):
        asert_dict = payload.dict(exclude_none=True)
        # 构造design_key
        design_key = "".join([payload.round_key, "-", payload.dut_key, '-', payload.design_key])
        # 查询当前key应该为多少
        test_demand_count = TestDemand.objects.filter(project__id=payload.project_id, design__key=design_key).count()
        key_string = ''.join([design_key, "-", str(test_demand_count)])
        # 查询当前各个前面节点的instance
        round_instance = Round.objects.get(project__id=payload.project_id, key=payload.round_key)
        dut_instance = Dut.objects.get(project__id=payload.project_id,
                                       key="".join([payload.round_key, "-", payload.dut_key]))
        design_instance = Design.objects.get(project__id=payload.project_id, key="".join(
            [payload.round_key, "-", payload.dut_key, '-', payload.design_key]))
        asert_dict.update({'key': key_string, 'round': round_instance, 'dut': dut_instance, 'design': design_instance,
                           'title': payload.name})
        asert_dict.pop("round_key")
        asert_dict.pop("dut_key")
        asert_dict.pop("design_key")
        asert_dict.pop("testContent")
        # 对标识进行处理，获取设计需求的标识，然后存入例如RS422
        asert_dict['ident'] = design_instance.ident
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        qs = TestDemand.objects.create(**asert_dict)
        # 对testContent单独处理
        data_list = []
        for item in payload.dict()["testContent"]:
            if not isinstance(item, dict):
                item = item.dict()
            item["testDemand"] = qs
            data_list.append(TestDemandContent(**item))
        TestDemandContent.objects.bulk_create(data_list)
        return qs

    # 更新测试需求
    @route.put("/testDemand/update/{id}", response=TestDemandCreateOutSchema, url_name="testDemand-update")
    @transaction.atomic
    def update_testDemand(self, id: int, payload: TestDemandCreateInputSchema):
        # 查到当前
        testDemand_qs = TestDemand.objects.get(id=id)
        for attr, value in payload.dict().items():
            if attr == 'project_id' or attr == 'round_key' or attr == 'dut_key' or attr == 'design_key':
                continue # 如果发现是key则不处理
            if attr == 'name':
                setattr(testDemand_qs, "title", value)
            # 找到attr为testContent的
            if attr == 'testContent':
                content_list = testDemand_qs.testQField.all()
                for content_single in content_list:
                    content_single.delete()
                # 添加测试项步骤
                data_list = []
                for item in value:
                    if item['testXuQiu'] or item['testYuQi']:
                        item["testDemand"] = testDemand_qs
                        data_list.append(TestDemandContent(**item))
                TestDemandContent.objects.bulk_create(data_list)
            setattr(testDemand_qs, attr, value)
        testDemand_qs.save()
        return testDemand_qs

    # 删除测试需求
    @route.delete("/testDemand/delete", url_name="design-delete")
    @transaction.atomic
    def delete_testDemand(self, data: DeleteSchema):
        # 根据其中一个id查询出dut_id
        test_demand_single = TestDemand.objects.filter(id=data.ids[0])[0]
        design_id = test_demand_single.design.id
        design_key = test_demand_single.design.key
        multi_delete_testDemand(data.ids, TestDemand)
        index = 0
        test_demand_all_qs = TestDemand.objects.filter(design__id=design_id)
        for single_qs in test_demand_all_qs:
            test_demand_key = "".join([design_key, '-', str(index)])
            single_qs.key = test_demand_key
            index = index + 1
            single_qs.save()
        return ChenResponse(message="测试需求删除成功！")

    # 查询一个项目的所以测试项
    @route.get("/testDemand/getRelatedTestDemand", url_name="design-getRelatedTestDemand")
    @transaction.atomic
    def getRelatedTestDemand(self, id: int, round: str):
        project_qs = get_object_or_404(Project, id=id)
        # 找出属于该轮次的所有测试项
        round_qs = project_qs.pField.filter(key=round).first()
        designs = round_qs.rsField.all()
        data_list = []
        for design in designs:
            design_dict = {'label': design.name, 'value': design.id, 'children': []}
            for test_item in design.dtField.all():
                test_item_dict = {'label': test_item.name, 'value': test_item.id}
                design_dict['children'].append(test_item_dict)
            data_list.append(design_dict)
        return ChenResponse(message='获取成功', data=data_list)

    # 处理desgin关联testDemand接口
    @route.post('/testDemand/solveRelatedTestDemand', url_name="design-solveRelatedTestDemand")
    @transaction.atomic
    def solveRelatedTestDemand(self, data: TestDemandRelatedSchema):
        test_item_ids = data.data
        non_exist_ids = [x for x in test_item_ids]
        project_qs = get_object_or_404(Project, id=data.project_id)
        key_str = "-".join([data.round_key, data.dut_key, data.design_key])
        design_item = project_qs.psField.filter(key=key_str).first()
        if design_item:
            # 将test_item_ids中本身具有的测试项从id数组中移除
            for test_id in test_item_ids:
                for ti in design_item.dtField.all():
                    if ti.pk == test_id:
                        non_exist_ids.remove(test_id)
            if len(non_exist_ids) <= 0 and len(test_item_ids) > 0:
                return ChenResponse(status=400, code=200, message='选择的测试项全部存在于当前设计需求中，请重新选择...')
            # 先查询现在有的关联测试项
            for item in design_item.odField.values('id'):
                item_id = item.get('id', None)
                if not item_id in test_item_ids:
                    test_item_obj = TestDemand.objects.filter(id=item_id).first()
                    design_item.odField.remove(test_item_obj)
            for test_item_id in non_exist_ids:
                test_items = design_item.odField.filter(id=test_item_id)
                if len(test_items) <= 0:
                    # 查询testDemand
                    design_item.odField.add(TestDemand.objects.filter(id=test_item_id).first())
        else:
            return ChenResponse(status=400, code=400, message='设计需求不存在，请检查...')
        return ChenResponse(status=200, code=200, message='添加关联测试项成功...')

    # 找出已关联的测试项给前端的cascader
    @route.post('/testDemand/getExistRelatedTestDemand', url_name="design-getExistRelatedTestDemand")
    @transaction.atomic
    def getExistRelatedTestDemand(self, data: TestDemandExistRelatedSchema):
        project_qs = get_object_or_404(Project, id=data.project_id)
        key_str = "-".join([data.round_key, data.dut_key, data.design_key])
        design_item = project_qs.psField.filter(key=key_str).first()
        ids = []
        if design_item:
            for item in design_item.odField.all():
                ids.append(item.id)
        return ids
