from datetime import date, timedelta
from ninja_extra import api_controller, ControllerBase, route
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Q
# 导入模型
from apps.project.models import Project, Dut, TestDemand
# 工具类函数
from apps.createDocument.extensions.util import create_bg_docx, get_round1_problem
from utils.util import get_str_dict, get_list_dict, create_problem_grade_str, create_str_testType_list, \
    create_demand_summary, create_problem_type_str, create_problem_table

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
        return create_bg_docx('测评完成情况.docx', context)

    # 生成综述
    @route.get('/create/summary', url_name='create-summary')
    def create_summary(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        # 找出所有问题单
        problem_qs = project_obj.projField.all()
        problem_grade_dict = {}
        problem_type_dict = {}
        # 建议问题统计
        problem_suggest_count = 0
        problem_suggest_solved_count = 0
        for problem in problem_qs:
            grade_key: str = get_str_dict(problem.grade, 'problemGrade')
            type_key: str = get_str_dict(problem.type, 'problemType')
            # 问题等级字典-计数
            if grade_key in problem_grade_dict.keys():
                problem_grade_dict[grade_key] += 1
            else:
                problem_grade_dict[grade_key] = 1
            # 问题类型字典-计数
            if type_key in problem_type_dict.keys():
                problem_type_dict[type_key] += 1
            else:
                problem_type_dict[type_key] = 1
            # 建议问题统计
            if problem.grade == '3':
                problem_suggest_count += 1
                if problem.status == '1':
                    problem_suggest_solved_count += 1
        problem_grade_list = []
        problem_type_list = []
        for key, value in problem_grade_dict.items():
            problem_grade_list.append("".join([f"{key}问题", f"{value}个"]))
        for key, value in problem_type_dict.items():
            problem_type_list.append("".join([f"{key}", f"{value}个"]))
        # 用来生成建议问题信息
        if problem_suggest_count > 0 and problem_suggest_count - problem_suggest_solved_count > 0:
            all_str = (f"测评过程中提出了{problem_suggest_count}个建议改进，"
                       f"其中{problem_suggest_solved_count}个建议改进已修改，"
                       f"剩余{problem_suggest_count - problem_suggest_solved_count}个未修改并经总体单位认可同意。")
        elif problem_suggest_count > 0 and problem_suggest_count - problem_suggest_solved_count == 0:
            all_str = (f"测评过程中提出了{problem_suggest_count}个建议改进，"
                       f"全部建议问题已修改")
        else:
            all_str = f"测评过程中未提出建议项。"

        context = {
            'problem_count': problem_qs.count(),
            'problem_grade_str': "、".join(problem_grade_list),
            'problem_type_str': '、'.join(problem_type_list),
            'all_str': all_str,
        }
        return create_bg_docx('综述.docx', context)

    # 生成测试内容和结果[报告非常关键的一环-大模块] TODO:以后考虑解耦
    @route.get('/create/contentandresults', url_name='create-contentandreasults')
    @transaction.atomic
    def create_content_results(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        project_ident = project_obj.ident
        # ~~~~首轮信息~~~~
        round1 = project_obj.pField.filter(key='0').first()  # !warning轮次1对象

        # 1.处理首轮文档名称
        doc_list = []
        round1_duts = round1.rdField.filter(Q(type='SJ') | Q(type='XQ') | Q(type='XY'))
        for dut in round1_duts:
            dut_dict = {
                'name': dut.name,
                'ident': dut.ref,
                'version': dut.version
            }
            doc_list.append(dut_dict)

        # 2.处理首轮文档问题的统计 - 注意去重
        problems = project_obj.projField.all().distinct()  # !important:大变量-项目所有问题
        problems_r1 = problems.filter(case__round__key='0')  # !important:大变量-首轮的所有问题
        problems_doc_r1 = problems_r1.filter(case__test__testType='8')  # 第一轮所有文档问题

        # 3.第一轮代码审查问题统计/版本
        source_r1_dut = round1.rdField.filter(type='SO').first()  # !warning:小变量-第一轮源代码对象
        program_r1_problems = problems_r1.filter(Q(case__test__testType='2') | Q(case__test__testType='3'))

        # 4.第一轮静态问题统计
        static_problems = problems_r1.filter(case__test__testType='15')

        # 5.第一轮动态测试用例个数(动态测试-非静态分析、文档审查、代码审查、代码走查4个)
        case_r1_qs = round1.rcField.filter(~Q(test__testType='2'), ~Q(test__testType='3'), ~Q(test__testType='8'),
                                           ~Q(test__testType='15'),
                                           round__key='0')  # !warning:中变量-第一轮动态测试用例qs
        testType_list, testType_count = create_str_testType_list(case_r1_qs)
        ## 动态测试(第一轮)各个类型测试用例执行表/各个测试需求表
        demand_r1_dynamic_qs = round1.rtField.filter(~Q(testType='2'), ~Q(testType='3'), ~Q(testType='8'),
                                                     ~Q(testType='15'))  # !warning:中变量:第一轮动态测试的测试项
        summary_r1_demand_info, summry_r1_demandType_info = create_demand_summary(demand_r1_dynamic_qs, project_ident)

        # N.第一轮所有动态问题统计
        problems_dynamic_r1 = problems_r1.filter(~Q(case__test__testType='2'), ~Q(case__test__testType='3'),
                                                 ~Q(case__test__testType='8'),
                                                 ~Q(case__test__testType='15'))  # !critical:大变量:第一轮动态问题单qs
        ## 为避免重复问题单:因为有case多对多，所以使用set
        problem_dynamic_r1_type_str = create_problem_type_str(problems_dynamic_r1)
        problem_dynamic_r1_grade_str = create_problem_grade_str(problems_dynamic_r1)

        context = {
            'project_name': project_obj.name,
            'doc_list': doc_list,
            'r1_problem_count': problems_doc_r1.count(),
            'r1_problem_str':
                f"{'，其中' + create_problem_grade_str(problems_doc_r1) if problems_doc_r1.count() > 0 else '即未发现问题'}",
            'r1_version': source_r1_dut.version if source_r1_dut else "未录入首轮版本信息",
            'r1_program_problem_count': program_r1_problems.count(),
            'r1_program_problem_str':
                f'{"，其中" + create_problem_grade_str(program_r1_problems) if program_r1_problems.count() > 0 else "即未发现问题"}',
            'r1_static_problem_count': static_problems.count(),
            'r1_static_problem_str': f"{'，其中' + create_problem_grade_str(static_problems) if static_problems.count() > 0 else '即未发现问题'}",
            'r1_case_count': case_r1_qs.count(),
            'r1_case_testType': "、".join(testType_list),
            'r1_case_testType_count': testType_count,
            'r1_problem_counts': len(problems_dynamic_r1),
            'r1_exe_info_all': summary_r1_demand_info,
            'r1_exe_info_type': summry_r1_demandType_info,
            'r1_dynamic_problem_str': problem_dynamic_r1_type_str,
            'r1_dynamic_problem_grade_str': problem_dynamic_r1_grade_str,
            'r1_problem_all_count': problems_r1.count(),
            'r1_problem_all_grade_str': f'{"，其中" + create_problem_grade_str(problems_r1) if problems_r1.count() > 0 else "即未发现问题"}',
            'r1_problem_closed_count': problems_r1.filter(status=1).count(),
            'r1_problem_noclosed_count': problems_r1.count() - problems_r1.filter(status=1).count(),
            'r1_problem_table': create_problem_table(problems_r1),
        }
        return create_bg_docx("测试内容和结果.docx", context)
