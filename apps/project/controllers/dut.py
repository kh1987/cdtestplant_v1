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
            dut_key = "".join([round_key, '-', str(index)])
            single_qs.key = dut_key
            single_qs.ident = ident_before_string + "UT" + str(index + 1)
            index = index + 1
            single_qs.save()
        return ChenResponse(message=message)

    # 查询项目中第一轮次是否存在源代码的被测件
    @route.get("/dut/soExist", url_name="dut-soExist")
    @transaction.atomic
    def delete_soExist(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        so_dut = project_obj.pdField.filter(round__key='0', type='SO')
        if so_dut:
            return ChenResponse(data={'exists': True}, code=200, status=200, message='检测到已有第一轮的源代码')
        else:
            return ChenResponse(data={'exists': False}, status=200)

    # 弹窗添加第一轮被测件源代码信息，另外创建测试项（静态分析、代码审查），测试用例（静态分析、代码审查）
    @route.post("/dut/createR1Sodut", response=DutCreateOutSchema, url_name='dut-r1SoDut')
    @transaction.atomic
    def create_r1_so_dut(self, data: DutCreateR1SoDutSchema):
        asert_dict = data.dict(exclude_none=True)
        project_obj = get_object_or_404(Project, id=data.project_id)
        if Dut.objects.filter(project__id=data.project_id, round__key='0', type='SO').exists():
            return ChenResponse(code=400, status=400, message='源代码被测件一个轮次只能添加一个')
        # 查询当前key应该为多少
        dut_count = Dut.objects.filter(project__id=data.project_id, round__key='0').count()
        key_string = ''.join(['0', "-", str(dut_count)])
        asert_dict['ident'] = "-".join([project_obj.ident, 'R1', 'UT', str(dut_count + 1)]).replace("UT-", "UT")
        # 查询round_id
        round_id = project_obj.pField.filter(key='0').first().id
        asert_dict['round_id'] = round_id
        asert_dict.update({'key': key_string, 'title': '软件源代码', 'type': 'SO', 'name': '软件源代码', 'level': '1'})
        dut_qs: Dut = Dut.objects.create(**asert_dict)
        # 到这里就逼迫用户创建了第一轮的so_dut
        # 1.现在要创建静态分析和代码审查设计需求（design2个）
        user_name = self.context.request.user.name
        # 1.1.自动创建design静态分析
        jt_design_create_dict = {
            'ident': 'JTFX',
            'name': '静态分析',
            'demandType': '6',
            'description': "对源代码程序进行静态分析",
            'title': '静态分析',
            'key': ''.join([dut_qs.key, '-', '0']),
            'level': '2',
            'chapter': '/',
            'project': project_obj,
            'round': dut_qs.round,
            'dut': dut_qs
        }
        new_design_jt: Design = Design.objects.create(**jt_design_create_dict)
        # 1.1.1.自动创建demand静态分析
        jt_demand_create_dict = {
            'ident': 'JTFX',
            'name': '静态分析',
            'adequacy': '对软件全部源程序进行进行质量度量、控制流分析、数据流分析的静态统计信息分析',
            'priority': '2',
            'testType': '15',
            'testMethod': '["3"]',
            'title': '静态分析',
            'key': ''.join([new_design_jt.key, '-', '0']),
            'level': '3',
            'project': project_obj,
            'round': new_design_jt.round,
            'dut': new_design_jt.dut,
            'design': new_design_jt,
        }
        new_demand_jt = TestDemand.objects.create(**jt_demand_create_dict)
        TestDemandContent.objects.create(testDemand=new_demand_jt, subName='静态分析',
                                         subDesc='对被测软件全部源程序进行静态分析，'
                                                 '对控制流、数据流进行分析，验证软件是否满足控制流和数据流要求。'
                                                 '依据质量特性需求统计质量度量信息',
                                         condition='已有被测件全部源代码',
                                         operation='使用LDRA '
                                                   'TestBed软件和Klocwork软件工具对被测软件全部源'
                                                   '程序进行静态分析，依据附录5对源程序进行检查。'
                                                   '\a1）使用静态分析工具统计软件质量度量信息，包含：'
                                                   '\a（1）软件总注释率不小于20'
                                                   '%（注释行数/软件规模*100%）；\a（2）'
                                                   '模块的平均规模不大于200行（模块代码行数之和/模块数）'
                                                   '；\a（3）模块的平均圈复杂度不大于10（模块圈复杂度之和/模块总数）'
                                                   '；\a（4）	'
                                                   '模块的平均扇出数不大于7（模块扇出数之和/模块总数）。'
                                                   '\a2）使用静态分析工具结合人工分析对控制流和数据流进行分析，'
                                                   '验证软件是否满足控制流和数据流要求。', )
        new_case_jt = Case.objects.create(
            ident='JTFX',
            name='静态分析',
            initialization='已获取全部被测件源代码程序，静态分析工具准备齐备',
            premise='提交的代码出自委托方受控库，是委托方正式签署外发的',
            summarize='依据委托方的要求进行静态分析，验证软件质量度量和编码规则是否满足军标要求',
            designPerson=user_name,
            testPerson=user_name,
            monitorPerson=user_name,
            project=project_obj,
            isLeaf=True,
            round=new_demand_jt.round,
            dut=new_demand_jt.dut,
            design=new_demand_jt.design,
            test=new_demand_jt,
            title='静态分析',
            key=''.join([new_demand_jt.key, '-', '0']),
            level='4'
        )
        CaseStep.objects.create(case=new_case_jt,
                                operation='使用LDRA TestBed软件和Klocwork软件工具对被测软件'
                                          '全部源程序进行静态分析，并配合人工以及检查单进行分析',
                                expect='静态审查单全部通过，且源代码满足编码规则和质量度量要求',
                                result='静态度量结果符合国军标要求，静态分析审查单全部通过', )
        # 1.2.自动创建代码审查design
        dm_design_create_dict = {
            'ident': 'DMSC',
            'name': '代码审查',
            'demandType': '6',
            'description': "对源码代码程序进行人工审查",
            'title': '代码审查',
            'key': ''.join([dut_qs.key, '-', '1']),
            'level': '2',
            'chapter': '/',
            'project': dut_qs.project,
            'round': dut_qs.round,
            'dut': dut_qs
        }
        new_design_dm = Design.objects.create(**dm_design_create_dict)
        dm_demand_create_dict = {
            'ident': 'DMSC',
            'name': '代码审查',
            'adequacy': '对软件全部源代码/重点模块进行代码审查',
            'priority': '2',
            'testType': '2',
            'testMethod': '["3"]',
            'title': '代码审查',
            'key': ''.join([new_design_dm.key, '-', '0']),
            'level': '3',
            'project': project_obj,
            'round': new_design_dm.round,
            'dut': new_design_dm.dut,
            'design': new_design_dm,
        }
        new_demand_dm = TestDemand.objects.create(**dm_demand_create_dict)
        TestDemandContent.objects.create(
            testDemand=new_demand_dm,
            subName='代码审查',
            subDesc='通过人工审查及借助工具辅助分析的方式开展代码审查，审查代码编程准则的符合性、'
                    '代码流程实现的正确性、代码结构的合理性以及代码实现需求的正确性；人工审查中发现的问题，审查人员应及时记录',
            condition='被测件源代码已获取',
            operation='人工审查及借助工具辅助分析的方式',
            observe='和依据附录代码审查单范围内的源代码开展四个方面的审查:\a',
            expect='1）编程准则检查：依据编程准则的要求，对程序的编码与编程准则进行符合性检查；\a'
                   '2）代码流程审查：审查程序代码的条件判别、控制流程、数据处理等满足设计要求；\a'
                   '3）软件结构审查：依据设计文档，审查程序代码的结构设计的合理性，包括程序结构设计和数据结构设计；\a'
                   '4）需求实现审查：依据需求文档及其他相关资料，审查程序代码的需求层的功能实现是否正确；\a'
        )
        new_case_dm = Case.objects.create(
            ident='DMSC',
            name='代码审查',
            initialization='代码已提交',
            premise='提交的代码出自委托方受控库，是委托方正式签署外发的',
            summarize='通过人工审查及借助工具辅助分析的方式开展代码审查，审查代码编程准则的符合性、'
                      '代码流程实现的正确性、代码结构的合理性以及代码实现需求的正确性；人工审查中发现的问题，审查人员应及时记录',
            designPerson=user_name,
            testPerson=user_name,
            monitorPerson=user_name,
            project=project_obj,
            isLeaf=True,
            round=new_demand_dm.round,
            dut=new_demand_dm.dut,
            design=new_demand_dm.design,
            test=new_demand_dm,
            title='代码审查',
            key=''.join([new_demand_dm.key, '-', '0']),
            level='4'
        )
        CaseStep.objects.create(case=new_case_dm,
                                operation='通过人工审查及借助工具辅助分析的方式开展代码审查，审查代码编程准则的符合性、'
                                          '代码流程实现的正确性、代码结构的合理性以及代码实现需求的正确性；'
                                          '人工审查中发现的问题，审查人员应及时记录',
                                expect='代码设计正确，满足审查单要求，无不符合项',
                                result='代码设计正确，满足审查单要求，无不符合项', )

        return dut_qs
