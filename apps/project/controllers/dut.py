import datetime
from copy import deepcopy
from ninja_extra import api_controller, ControllerBase, route
from ninja import Query
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated
from ninja.pagination import paginate
from utils.chen_pagination import MyPagination
from django.db import transaction
from typing import List
from utils.chen_response import ChenResponse
from utils.chen_crud import multi_delete_dut
from utils.codes import HTTP_INDEX_ERROR
from apps.project.models import Dut, Round, Project, Design, TestDemand, TestDemandContent, Case, CaseStep
from django.shortcuts import get_object_or_404
from apps.project.schemas.dut import DutModelOutSchema, DutFilterSchema, DutTreeReturnSchema, DutTreeInputSchema, \
    DutCreateInputSchema, DutCreateOutSchema, DeleteSchema, DutCreateR1SoDutSchema
# 导入自动生成design、demand、case的辅助函数
from apps.project.tools.auto_create_data import auto_create_jt_and_dm, auto_create_wd
from apps.project.tools.delete_change_key import dut_delete_sub_node_key

@api_controller("/project", auth=JWTAuth(), permissions=[IsAuthenticated], tags=['被测件数据'])
class DutController(ControllerBase):
    @route.get("/getDutList", response=List[DutModelOutSchema], exclude_none=True, url_name="dut-list")
    @transaction.atomic
    @paginate(MyPagination)
    def get_dut_list(self, filters: DutFilterSchema = Query(...)):
        for attr, value in filters.__dict__.items():
            if getattr(filters, attr) is None:
                setattr(filters, attr, '')
        qs = Dut.objects.filter(project__id=filters.project_id, round__key=filters.round_id,
                                ident__icontains=filters.ident,
                                name__icontains=filters.name,
                                type__contains=filters.type, version__icontains=filters.version,
                                release_union__icontains=filters.release_union).order_by("-create_datetime")
        return qs

    # 处理树状数据
    @route.get("/getDutInfo", response=List[DutTreeReturnSchema], url_name="dut-info")
    def get_round_tree(self, payload: DutTreeInputSchema = Query(...)):
        qs = Dut.objects.filter(project__id=payload.project_id, round__key=payload.key)
        return qs

    # 添加被测件
    @route.post("/dut/save", url_name="dut-create", response=DutCreateOutSchema)
    @transaction.atomic
    def create_dut(self, payload: DutCreateInputSchema):
        asert_dict = payload.dict(exclude_none=True)
        # 当被测件为SO时，一个轮次只运行有一个
        if payload.type == 'SO':
            if Dut.objects.filter(project__id=payload.project_id, round__key=payload.round_key, type='SO').exists():
                return ChenResponse(code=400, status=400, message='源代码被测件一个轮次只能添加一个')
        # 判重标识
        if Dut.objects.filter(project__id=payload.project_id, round__key=payload.round_key,
                              ident=payload.ident).exists():
            return ChenResponse(code=400, status=400, message='被测件的标识重复，请检查')
        # 查询当前key应该为多少
        dut_count = Dut.objects.filter(project__id=payload.project_id, round__key=payload.round_key).count()
        key_string = ''.join([payload.round_key, "-", str(dut_count)])
        # 然后在标识后面加上UT+KEY -> 注意删除时也改了key要对应修改blink1->>>>>>
        asert_dict['ident'] = ''.join([asert_dict['ident'], str(dut_count + 1)])
        # 查询当前的round_id
        round_instance = Round.objects.get(project__id=payload.project_id, key=payload.round_key)
        asert_dict.update({'key': key_string, 'round': round_instance, 'title': payload.name})
        asert_dict.pop("round_key")
        qs = Dut.objects.create(**asert_dict)
        return qs

    # 更新被测件
    @route.put("/dut/update/{id}", url_name="dut-update", response=DutCreateOutSchema)
    @transaction.atomic
    def update_dut(self, id: int, payload: DutCreateInputSchema):
        dut_search = Dut.objects.filter(project__id=payload.project_id, ident=payload.ident)
        # 判断是否和同项目同轮次的标识重复
        if len(dut_search) > 1:
            return ChenResponse(code=400, status=400, message='被测件的标识重复，请检查')
        # 查到当前
        if payload.type == 'SO':
            dut_qs = Dut.objects.get(id=id)
            for attr, value in payload.dict().items():
                if attr == 'project_id' or attr == 'round_key':
                    continue
                if attr == 'name':
                    setattr(dut_qs, "title", value)
                setattr(dut_qs, attr, value)
            dut_qs.save()
            return dut_qs
        else:
            dut_qs = Dut.objects.get(id=id)
            for attr, value in payload.dict().items():
                if attr == 'project_id' or attr == 'round_key':
                    continue
                if attr == 'black_line' or attr == 'code_line' or attr == 'mix_line' or attr == 'comment_line':
                    setattr(dut_qs, attr, "")
                    continue
                if attr == 'name':
                    setattr(dut_qs, "title", value)
                setattr(dut_qs, attr, value)
            dut_qs.save()
            return dut_qs

    # 删除被测件 - 1.重新对key排序 2.重新对表示尾号排序
    @route.delete("/dut/delete", url_name="dut-delete")
    @transaction.atomic
    def delete_dut(self, data: DeleteSchema):
        # 查询某一个dut对象
        try:
            dut_single = Dut.objects.filter(id=data.ids[0])[0]
        except IndexError:
            return ChenResponse(status=500, code=HTTP_INDEX_ERROR, message='您未选择需要删除的内容')
        # 查询出dut所属的轮次id、key
        round_id = dut_single.round.id
        round_key = dut_single.round.key
        # blink1->>>>>> 这里不仅重排key，还要重排ident中编号,先取出前面的RXXXX-RX等信息,这里必须要在删除之前
        # 查询出当前轮次所有dut
        ids = deepcopy(data.ids)
        message = '被测件删除成功'
        for id in data.ids:
            dut_obj = Dut.objects.filter(type='SO', id=id).first()
            if dut_obj:
                ids.remove(id)
                message = '源代码被测件不能删除，其他被测件删除成功...'
        multi_delete_dut(ids, Dut)
        dut_all_qs = Dut.objects.filter(round__id=round_id)
        ident_before_string = dut_all_qs[0].ident.split("UT")[0]  # 输出类似于“R2233-R1-”
        index = 0
        for single_qs in dut_all_qs:
            dut_key = "".join([round_key, '-', str(index)])  # 重排现有的dut的key
            single_qs.key = dut_key
            single_qs.ident = ident_before_string + "UT" + str(index + 1)
            index = index + 1
            single_qs.save()
            # 不仅重排自己的还要改所有子类的key，因为还是之前的key
            dut_delete_sub_node_key(single_qs)

        return ChenResponse(message=message)

    # 查询项目中第一轮次是否存在源代码的被测件 -> 5月16日更改：查每一轮是否有源代码被测件
    @route.get("/dut/soExist", url_name="dut-soExist")
    @transaction.atomic
    def delete_soExist(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        # 先查询项目的所有轮次
        round_qs = project_obj.pField.all()
        data = {
            'round_count': round_qs.count(),
            'round_list': []
        }
        for round_obj in round_qs:
            so_dut_exists = round_obj.rdField.filter(type='SO').exists()
            round_dict = {
                'key': round_obj.key,
                'isExists': so_dut_exists
            }
            data['round_list'].append(round_dict)
        return ChenResponse(code=200, status=200, message='在data展示轮次是否有源代码信息', data=data)

    # 弹窗添加第一轮被测件源代码信息，另外创建测试项（静态分析、代码审查），测试用例（静态分析、代码审查）
    @route.post("/dut/createR1Sodut", response=DutCreateOutSchema, url_name='dut-r1SoDut')
    @transaction.atomic
    def create_r1_so_dut(self, data: DutCreateR1SoDutSchema):
        asert_dict = data.dict(exclude_none=True)  # asert_dict['round_key']可以获取是第几轮次
        round_key = asert_dict.pop('round_key')
        project_obj = get_object_or_404(Project, id=data.project_id)
        if Dut.objects.filter(project__id=data.project_id, round__key=round_key, type='SO').exists():
            return ChenResponse(code=400, status=400, message='源代码被测件一个轮次只能添加一个')
        # 查询当前key应该为多少
        dut_count = Dut.objects.filter(project__id=data.project_id, round__key=round_key).count()
        key_string = ''.join([round_key, "-", str(dut_count)])
        asert_dict['ident'] = "-".join([project_obj.ident, ''.join(['R', str(int(round_key) + 1)]), 'UT', str(dut_count + 1)]).replace("UT-", "UT")
        # 查询round_id
        round_id = project_obj.pField.filter(key=round_key).first().id
        asert_dict['round_id'] = round_id
        asert_dict.update({'key': key_string, 'title': '软件源代码', 'type': 'SO', 'name': '软件源代码', 'level': '1'})
        dut_qs: Dut = Dut.objects.create(**asert_dict)
        # 到这里就自动生成了第一轮的源代码dut，下面使用辅助函数自动生成（静态分析、代码审查）
        user_name = self.context.request.user.name
        # 1.自动生成静态分析、代码审查
        auto_create_jt_and_dm(user_name, dut_qs, project_obj)
        # 2.自动生成文档审查在源代码被测件中
        auto_create_wd(user_name, dut_qs, project_obj)
        return dut_qs
