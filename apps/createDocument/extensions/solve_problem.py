import base64
import io
from apps.project.models import Problem
from utils.util import get_str_dict
from docxtpl import InlineImage
from docx.shared import Mm
from utils.util import MyHTMLParser
from apps.createDocument.extensions.parse_rich_text import RichParser

def parse_html(html_txt, a_list, doc):
    """解析HTML字段的文字和图片到列表,输入是HTML字段的txt以及列表，输出列表"""
    parser = RichParser(html_txt)
    a_list.extend(parser.get_final_list(doc, img_size=100))
    return a_list

def create_one_problem_dit(problem: Problem, problem_prefix: str, doc) -> dict:
    """问题单汇总表每个问题作为一行的数据"""
    problem_dict = {
        'ident': '_'.join([problem_prefix, problem.ident]),
        'grade': get_str_dict(problem.grade, 'problemGrade'),
        'type': get_str_dict(problem.type, 'problemType'),
        'status': get_str_dict(problem.status, 'problemStatu')
    }
    # 问题操作 - HTML解析
    desc_list = ['【问题描述】']
    desc_list = parse_html(problem.operation, desc_list, doc)
    desc_list_yq = ['\a【问题影响】']
    desc_list_yq = parse_html(problem.result, desc_list_yq, doc)
    desc_list.extend(desc_list_yq)
    problem_dict['desciption'] = desc_list
    # 问题处理方式表格单元格
    solve_list = ['【原因分析】']
    solve_list = parse_html(problem.analysis, solve_list, doc)
    solve_list_effect = ['\a【影响域】']
    solve_list_effect = parse_html(problem.effect_scope, solve_list_effect, doc)
    solve_list_basic = ['\a【处理方式】', problem.solve]
    solve_list_verify = ['\a【回归验证】']
    solve_list_verify = parse_html(problem.verify_result, solve_list_verify, doc)
    solve_list.extend(solve_list_effect)
    solve_list.extend(solve_list_basic)
    solve_list.extend(solve_list_verify)
    problem_dict['solve'] = solve_list
    return problem_dict
