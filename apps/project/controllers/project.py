from pathlib import Path
from datetime import date
from typing import List
from shutil import copytree, rmtree
from django.shortcuts import get_object_or_404
from django.db import transaction
from ninja_extra import api_controller, ControllerBase, route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from utils.chen_pagination import MyPagination
from ninja.pagination import paginate
from ninja import Query
from utils.chen_response import ChenResponse
from utils.chen_crud import create, multi_delete_project
from apps.project.models import Project, Round
from apps.project.schemas.project import ProjectRetrieveSchema, ProjectFilterSchema, ProjectCreateInput, DeleteSchema
from utils.util import get_str_dict

media_path = Path.cwd() / 'media'
base_document_path = Path.cwd() / 'conf/base_document'

@api_controller("/testmanage/project", auth=JWTAuth(), permissions=[IsAuthenticated], tags=['项目表相关'])
class ProjectController(ControllerBase):
    @route.get("/index", response=List[ProjectRetrieveSchema])
    @paginate(MyPagination)
    def list_project(self, filters: ProjectFilterSchema = Query(...)):
        for attr, value in filters.__dict__.items():
            if getattr(filters, attr) is None:
                setattr(filters, attr, '')
        # 处理时间范围
        start_time = self.context.request.GET.get('searchOnlyTimeRange[0]')
        if start_time is None:
            start_time = "2000-01-01"
        end_time = self.context.request.GET.get('searchOnlyTimeRange[1]')
        if end_time is None:
            end_time = '9999-01-01'
        date_list = [start_time, end_time]
        # 前端返回的member
        member_list = []
        for key, value in self.context.request.GET.items():
            if key.find('member') != -1:
                member_list.append(self.context.request.GET[key])
        qs = Project.objects.filter(
            ident__icontains=filters.ident, name__icontains=filters.name,
            beginTime__range=date_list, duty_person__icontains=filters.duty_person,
            security_level__icontains=filters.security_level,
            report_type__icontains=filters.report_type, step__icontains=filters.step,
            member__contains=member_list).order_by(
            "-create_datetime")
        # 对软件类型进行处理
        if filters.soft_type != '':
            qs = qs.filter(soft_type=filters.soft_type)
        return qs

    @route.post("/save")
    @transaction.atomic
    def create_project(self, data: ProjectCreateInput):
        data_dict = data.dict()
        ident_qucover = Project.objects.filter(ident=data.dict()['ident'])
        if ident_qucover:
            return ChenResponse(code=400, status=400, message="项目标识重复，请重新设置")
        qs = create(self.context.request, data_dict, Project)
        # 创建项目时候添加第一轮测试
        if qs:
            Round.objects.create(project_id=qs.id, key='0', level='0', title='第1轮测试', name='第1轮测试',
                                 remark='第一轮测试', ident=''.join([qs.ident, '-R1']))
            # 在新增项目时，将/conf/base_document 移动到 /media/{项目ident}/下面
            src_dir = base_document_path
            dist_dir = media_path / qs.ident
            copytree(src_dir, dist_dir)  # shutil模块直接是复制并命名，如果命名文件存在则抛出FileExists异常
            return ChenResponse(code=200, status=200, message="添加项目成功，并添加第一轮测试")

    @route.put("/update/{project_id}")
    @transaction.atomic
    def update_project(self, project_id: int, payload: ProjectCreateInput):
        project = self.get_object_or_exception(Project, id=project_id)
        ident = project.ident
        # 更新操作
        for attr, value in payload.dict().items():
            # setattr针对的是class
            setattr(project, attr, value)
        project.save()
        old_ident = ident
        new_ident = project.ident
        # 更新项目时判断ident是否修改，如果修改则需要改动media里面文件夹名字
        if project.ident != ident:
            try:
                Path(media_path / ident).rename(media_path / project.ident)
                # 同时要更改round和dut的标识
                for r in project.pField.all():
                    r.ident = r.ident.replace(old_ident, new_ident)
                    r.save()
                for d in project.pdField.all():
                    d.ident = d.ident.replace(old_ident, new_ident)
                    d.save()
            except PermissionError:
                return ChenResponse(code=500, status=500, message="请关闭文件资源管理器再试")
        return ChenResponse(code=200, status=200, message="项目更新成功")

    @route.delete("/delete")
    @transaction.atomic
    def delete(self, data: DeleteSchema):
        idents = multi_delete_project(data.ids, Project)
        # 查询media所属项目文件夹，并删除
        for ident in idents:
            project_media_path = media_path / ident
            rmtree(project_media_path)
        return ChenResponse(message="删除成功！")

    # 看板页面接口
    @route.get('/board')
    @transaction.atomic
    def board(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        # 1.项目阶段直接转字符串
        step_str = get_str_dict(project_obj.step, 'step')
        # 2.返回时间信息
        # 3.返回人员信息
        # 4.返回研制方信息
        # 5.返回用例信息
        case_qs = project_obj.pcField.all()
        exe_count = 0
        noexe_count = 0
        partexe_count = 0
        ## 5.1 计算已执行的用例数
        for case in case_qs:
            exe_flag = True
            part_flag = 0
            for case_step in case.step.all():
                if case_step.status != '1':
                    exe_flag = False
                else:
                    part_flag += 1
            if exe_flag:
                exe_count += 1
            else:
                if part_flag == case.step.count():
                    noexe_count += 1
                else:
                    partexe_count += 1
        # 6.计算问题单数
        problems = project_obj.projField.all()
        close_count = 0
        open_count = 0
        for problem in problems:
            if problem.status != '1':
                open_count += 1
            else:
                close_count += 1

        # 7.将时间提取 todo:后续将计算的事件放入该页面
        timers = {'round_time': []}
        rounds = project_obj.pField.all()
        timers['start_time'] = project_obj.beginTime
        timers['end_time'] = project_obj.endTime
        for round in rounds:
            round_number = int(round.key) + 1
            timers['round_time'].append({
                'name': f'第{round_number}轮次',
                'start': round.beginTime,
                'end': round.endTime
            })

        # 8.提取所有需求下面测试项、用例数量
        # 9.提取测试类型下面测试项数量、用例数量
        data_list = []
        for round in rounds:
            round_dict = {'name': f'第{int(round.key) + 1}轮次', 'desings': [], 'method_demand': {}, 'method_case': {}}
            designs = round.dsField.all()
            for design in designs:
                design_dict = {
                    'name': design.name,
                    'demand_count': design.dtField.count(),
                    'case_count': design.dcField.count()
                }
                round_dict['desings'].append(design_dict)
            demands = round.rtField.all()
            for demand in demands:
                test_type = get_str_dict(demand.testType, 'testType')
                if test_type not in round_dict['method_demand']:
                    round_dict['method_demand'][test_type] = 1
                else:
                    round_dict['method_demand'][test_type] += 1
            cases = round.rcField.all()
            for case in cases:
                testDemand = case.test
                case_type = get_str_dict(testDemand.testType, 'testType')
                if case_type not in round_dict['method_case']:
                    round_dict['method_case'][case_type] = 1
                else:
                    round_dict['method_case'][case_type] += 1
            data_list.append(round_dict)

        return {
            'ident': project_obj.ident,
            'name': project_obj.name,
            'step': step_str,
            'title_info': {
                '时间': {
                    '开始时间': project_obj.beginTime,
                    '结束时间': project_obj.endTime,
                    '到现在时间': f"{(date.today() - project_obj.beginTime).days}天",
                },
                '人员': {
                    '负责人': project_obj.duty_person,
                    '成员数': len(project_obj.member),
                },
                '开发方信息': {
                    '联系人': project_obj.dev_contact,
                    '电话': project_obj.dev_contact_phone,
                    '邮箱': project_obj.dev_email
                },
                '用例数': {
                    '总数': case_qs.count(),
                    '已执行': exe_count,
                    '未执行': noexe_count,
                    '部分执行': partexe_count,
                },
                '问题数': {
                    '总数': problems.count(),
                    '已闭环': close_count,
                    '未闭环': open_count,
                }
            },
            'time_line': timers,
            'statistics': data_list,
        }
