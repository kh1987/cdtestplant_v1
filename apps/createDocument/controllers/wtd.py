# 导入内置模块
from pathlib import Path
import io
import base64
# 导入django、ninja等模块
from ninja_extra import api_controller, ControllerBase, route
from django.db import transaction
from django.shortcuts import get_object_or_404
# 导入文档处理模块
from docxtpl import InlineImage, DocxTemplate
from docx.shared import Mm
# 导入ORM模型
from apps.project.models import Project, Dut, Round
# 导入工具
from utils.util import get_str_abbr, get_str_dict, MyHTMLParser
from utils.chen_response import ChenResponse

# @api_controller("/generateWtd", tags=['生成问题单文档系列'], auth=JWTAuth(), permissions=[IsAuthenticated])
@api_controller('/generateWtd', tags=['生成问题单文档系列'])
class GenerateControllerWtd(ControllerBase):
    @route.get("/create/problem", url_name="create-problem")
    @transaction.atomic
    def create_problem(self, id: int):
        tpl_path = Path.cwd() / 'media/form_template/wtd' / '问题详情表.docx'
        doc = DocxTemplate(tpl_path)
        """生成问题单"""
        project_obj = get_object_or_404(Project, id=id)
        problem_list = list(project_obj.projField.distinct())
        problem_list.sort(key=lambda x: int(x.ident))
        data_list = []
        for problem in problem_list:
            problem_dict = {'ident': problem.ident}
            # 1.生成被测对象名称、被测对象标识、被测对象版本
            cases = problem.case.all()
            str_dut_name_list = []
            str_dut_ident_list = []
            str_dut_version_list = []
            # 2.所属用例标识
            case_ident_list = []
            for case in cases:
                if case.test.testType == '8':
                    # 1.1.如果为文档审查，提取所属文档名称、文档被测件标识、文档被测件版本
                    str_dut_name_list.append(case.dut.name)
                    str_dut_ident_list.append(case.dut.ident)
                    str_dut_version_list.append(case.dut.version)
                else:
                    # 1.2.如果不为文档审查，则提取该轮次源代码dut的信息
                    so_dut = case.round.rdField.filter(type='SO').first()
                    if so_dut:
                        str_dut_name_list.append(project_obj.name + '软件')
                        str_dut_ident_list.append(so_dut.ref)
                        str_dut_version_list.append(so_dut.version)
                # 2.用例标识
                design = case.design  # 中间变量
                design_ident = design.ident  # RS422
                demand = case.test  # 中间变量
                demand_index = demand.key[-1]  # 2
                demand_testType = demand.testType  # 中间变量
                testType_abbr = get_str_abbr(demand_testType, 'testType')  # FT
                case_ident_list.append("_".join(
                    ['YL', design_ident, testType_abbr, str(int(demand_index) + 1).rjust(3, '0'),
                     str(int(case.key[-1]) + 1).rjust(3, '0')]))

            problem_dict['duts_name'] = "/".join(set(str_dut_name_list))
            problem_dict['duts_ref'] = "/".join(set(str_dut_ident_list))
            problem_dict['duts_version'] = "/".join(set(str_dut_version_list))
            problem_dict['case_ident'] = "，".join(set(case_ident_list))
            problem_dict['type'] = get_str_dict(problem.type, 'problemType')
            problem_dict['grade'] = get_str_dict(problem.grade, 'problemGrade')

            # 问题操作 - HTML解析
            parser = MyHTMLParser()
            parser.feed(problem.operation)
            desc_list = ['问题操作：']
            for strOrList in parser.allStrList:
                if strOrList.startswith("data:image/png;base64"):
                    base64_bytes = base64.b64decode(strOrList.replace("data:image/png;base64,", ""))
                    desc_list.append(InlineImage(doc, io.BytesIO(base64_bytes), width=Mm(90)))
                else:
                    desc_list.append(strOrList)
            desc_list_yq = ['\a预期描述：', problem.expect]
            desc_list.extend(desc_list_yq)
            parser2 = MyHTMLParser()
            parser2.feed(problem.result)
            desc_list_2 = ['\a问题结果：']
            for strOrList in parser2.allStrList:
                if strOrList.startswith("data:image/png;base64"):
                    base64_bytes = base64.b64decode(strOrList.replace("data:image/png;base64,", ""))
                    desc_list_2.append(InlineImage(doc, io.BytesIO(base64_bytes), width=Mm(90)))
                else:
                    desc_list_2.append(strOrList)
            desc_list.extend(desc_list_2)
            # 问题描述
            problem_dict['desc'] = desc_list
            # 问题建议
            problem_dict['suggest'] = problem.suggest
            problem_dict['postPerson'] = problem.postPerson
            problem_dict['postDate'] = problem.postDate
            close_str = '□修改文档        □修改程序        □不修改'
            if len(problem.closeMethod) < 1:
                close_str = '□修改文档        □修改程序        ■不修改'
            elif len(problem.closeMethod) == 2:
                close_str = '■修改文档        ■修改程序        □不修改'
            else:
                if problem.closeMethod[0] == '1':
                    close_str = '■修改文档        □修改程序        □不修改'
                elif problem.closeMethod[0] == '2':
                    close_str = '□修改文档        ■修改程序        □不修改'
                else:
                    close_str = '□修改文档        □修改程序        □不修改'
            problem_dict['closeMethod'] = close_str
            problem_dict['solve'] = problem.solve.replace('\n', '\a') if problem.solve else ""
            problem_dict['designer'] = problem.designerPerson
            problem_dict['designDate'] = problem.designDate
            # 闭环版本，当前轮次的下一个轮次闭环
            current_round = Round.objects.filter(rcQuery__caseQuery=problem).first()
            if current_round:
                # 找到下一个轮次
                next_round_key = str(int(current_round.key) + 1)
                next_round: Round = Round.objects.filter(key=next_round_key).first()
                if next_round:
                    # 1.判断是否为文档问题
                    so_dut: Dut = next_round.rdField.filter(type='SO').first()
                    if so_dut:
                        problem_dict['closeVersion'] = so_dut.version
            if 'closeVersion' not in problem_dict.keys():
                problem_dict['closeVersion'] = "$未找到闭环版本$"
            problem_dict['verifyPerson'] = problem.verifyPerson
            problem_dict['verifyDate'] = problem.verifyDate
            data_list.append(problem_dict)

        context = {
            'project_name': project_obj.name,
            'project_ident': project_obj.ident,
            'problem_list': data_list,
        }
        doc.render(context)
        try:
            doc.save(Path.cwd() / "media/output_dir/wtd" / '问题详情表.docx')
            return ChenResponse(status=200, code=200, message="文档生成成功！")
        except PermissionError as e:
            return ChenResponse(status=400, code=400, message="模版文件已打开，请关闭后再试，{0}".format(e))
