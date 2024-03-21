from datetime import date, timedelta
from ninja_extra import api_controller, ControllerBase, route
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
# 导入模型
from apps.project.models import Project, Dut, TestDemand
# 工具类函数
from apps.createDocument.extensions.util import create_bg_docx
from utils.util import get_str_dict, get_list_dict
from apps.createDocument.extensions.util import get_round1_problem

# @api_controller("/generateBG", tags=['生成报告文档系列'], auth=JWTAuth(), permissions=[IsAuthenticated])
@api_controller("/generateBG", tags=['生成报告文档系列'])
class GenerateControllerBG(ControllerBase):
    @route.get("/create/techyiju", url_name="create-techyiju")
    @transaction.atomic
    def create_techyiju(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        duties_qs = project_obj.pdField.filter(Q(type='XQ') | Q(type='SJ') | Q(type='XY'))
        std_documents = []
        for duty in duties_qs:
            one_duty = {'doc_name': duty.name, 'ident_version': duty.ref + '-' + duty.version,
                        'publish_date': duty.release_date, 'source': duty.release_union}
            std_documents.append(one_duty)
        # 添加大纲到这里
        ## 判断是否为鉴定
        doc_name = f'{project_obj.name}软件测评大纲'
        if project_obj.report_type == '9':
            doc_name = f'{project_obj.name}软件鉴定测评大纲'
        # 这里大纲版本升级如何处理 - TODO：1.大纲版本升级后版本处理 2.大纲时间如何处理？
        dg_duty = {'doc_name': doc_name, 'ident_version': f'PT-{project_obj.ident}-TO-1.00',
                   'publish_date': '2024-03-17', 'source': project_obj.test_unit}
        std_documents.append(dg_duty)

        # 需要添加说明、记录 - TODO：1.说明/记录版本升级后版本处理 2.说明/记录时间如何处理？
        sm_duty = {'doc_name': f'{project_obj.name}软件测试说明', 'ident_version': f'PT-{project_obj.ident}-TD-1.00',
                   'publish_date': '2024-03-22', 'source': project_obj.test_unit}
        jl_duty = {'doc_name': f'{project_obj.name}软件测试记录', 'ident_version': f'PT-{project_obj.ident}-TN',
                   'publish_date': '2024-03-28', 'source': project_obj.test_unit}
        hsm_duty = {'doc_name': f'{project_obj.name}软件回归测试说明',
                    'ident_version': f'PT-{project_obj.ident}-TD2-1.00',
                    'publish_date': '2024-03-29', 'source': project_obj.test_unit}
        hjl_duty = {'doc_name': f'{project_obj.name}软件回归测试记录',
                    'ident_version': f'PT-{project_obj.ident}-TN2',
                    'publish_date': '2024-04-08', 'source': project_obj.test_unit}
        std_documents.extend([sm_duty, jl_duty, hsm_duty, hjl_duty])
        # 生成二级文档
        context = {
            'std_documents': std_documents
        }
        return create_bg_docx("技术依据文件.docx", context)

    @route.get('/create/timeaddress')
    @transaction.atomic
    def create_timeaddress(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        bg_generate_date = date.today()
        begin_time = project_obj.beginTime
        # 研制单位名称+'实验室'为地点
        dynamit_location = project_obj.dev_unit + '实验室'
        context = {
            'begin_year': begin_time.year,
            'begin_month': begin_time.month,
            'end_year': bg_generate_date.year,
            'end_month': bg_generate_date.month,
            'begin_time': begin_time.strftime('%Y%m%d'),
            'end_time': bg_generate_date.strftime('%Y%m%d'),
            'dynamit_location': dynamit_location,
            'dg_weave_start_date': (begin_time + timedelta(days=1)).strftime('%Y%m%d'),
            'dg_weave_end_date': (begin_time + timedelta(days=6)).strftime('%Y%m%d'),
            'sj_weave_start_date': (begin_time + timedelta(days=7)).strftime('%Y%m%d'),
            'sj_weave_end_date': (begin_time + timedelta(days=14)).strftime('%Y%m%d'),
            'exe_weave_start_date': (begin_time + timedelta(days=15)).strftime('%Y%m%d'),
            'exe_weave_end_date': (begin_time + timedelta(days=31)).strftime('%Y%m%d'),
            'summary_start_date': (begin_time + timedelta(days=32)).strftime('%Y%m%d'),
        }
        return create_bg_docx('测评时间和地点.docx', context)

    # 在报告生成多个版本被测软件基本信息
    @route.get('/create/baseInformation', url_name='create-baseInformation')
    def create_information(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        languages = get_list_dict('language', project_obj.language)
        language_list = []
        for language in languages:
            language_list.append(language.get('ident_version'))

        # 获取轮次
        rounds = project_obj.pField.all()
        round_list = []
        for r in rounds:
            round_dict = {}
            # 获取SO的dut
            so_dut: Dut = r.rdField.filter(type='SO').first()
            if so_dut:
                round_dict['version'] = so_dut.version
                round_dict['line_count'] = so_dut.total_code_line
                round_list.append(round_dict)

        context = {
            'project_name': project_obj.name,
            'soft_type': project_obj.get_soft_type_display(),
            'security_level': get_str_dict(project_obj.security_level, 'security_level'),
            'runtime': get_str_dict(project_obj.runtime, 'runtime'),
            'devplant': get_str_dict(project_obj.devplant, 'devplant'),
            'language': "\a".join(language_list),
            'recv_date': project_obj.beginTime.strftime("%Y-%m-%d"),
            'dev_unit': project_obj.dev_unit,
            'version_info': round_list
        }
        return create_bg_docx('被测软件基本信息.docx', context)

    # 生成测评完成情况
    @route.get('/create/completionstatus', url_name='create-completionstatus')
    def create_completionstatus(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        # 找到第一轮轮次对象、第二轮轮次对象
        round1 = project_obj.pField.filter(key='0').first()
        round2 = project_obj.pField.filter(key='1').first()
        # 第一轮用例个数
        round1_case_qs = round1.rcField.all()
        # 这部分找出第一轮的所以测试类型，输出字符串，并排序
        test_type_set: set = set()
        for case in round1_case_qs:
            demand: TestDemand = case.test
            test_type_set.add(demand.testType)
        round1_testType_list = list(map(lambda x: x['ident_version'], get_list_dict('testType', list(test_type_set))))
        # 这里找出第一轮，源代码被测件，并获取版本
        so_dut = round1.rdField.filter(type='SO').first()
        so_dut_verson = "$请添加第一轮的源代码信息$"
        if so_dut:
            so_dut_verson = so_dut.version
        # 这里找出第二轮，源代码被测件，并获取版本
        round2_version = "$请添加第二轮的源代码信息$"
        if round2:
            so_dut_2: Dut = round2.rdField.filter(type='SO').first()
            if so_dut_2:
                round2_version = so_dut_2.version
        # 这部分找到第一轮的问题
        problem_qs = get_round1_problem(project_obj)
        context = {
            'is_JD': True if project_obj.report_type == '9' else False,
            'project_name': project_obj.name,
            'start_time_year': project_obj.beginTime.year,
            'start_time_month': project_obj.beginTime.month,
            'round1_case_count': round1_case_qs.count(),
            'round1_testType_str': '、'.join(round1_testType_list),
            'round1_version': so_dut_verson,
            'round1_problem_count': len(problem_qs),
            'round2_version': round2_version,
            'end_time_year': date.today().year,
            'end_time_month': date.today().month
        }
        print(context)
        return create_bg_docx('测评完成情况.docx', context)
