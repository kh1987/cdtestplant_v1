import base64
import io
from apps.project.models import Problem
from utils.util import get_str_dict
from docxtpl import InlineImage
from docx.shared import Mm
from utils.util import MyHTMLParser

def create_one_problem_dit(problem: Problem, problem_prefix: str, doc) -> dict:
    problem_dict = {
        'ident': '_'.join([problem_prefix, problem.ident]),
        'grade': get_str_dict(problem.grade, 'problemGrade'),
        'type': get_str_dict(problem.type, 'problemType'),
        'solve': problem.solve if problem.solve else "",
        'status': get_str_dict(problem.status, 'problemStatu')
    }
    # 问题操作 - HTML解析
    parser = MyHTMLParser()
    parser.feed(problem.operation)
    desc_list = ['问题操作：']
    for strOrList in parser.allStrList:
        if strOrList.startswith("data:image/png;base64"):
            base64_bytes = base64.b64decode(strOrList.replace("data:image/png;base64,", ""))
            # ~~~设置了固定宽度~~~
            desc_list.append(InlineImage(doc, io.BytesIO(base64_bytes), width=Mm(50)))
        else:
            desc_list.append(strOrList)

    desc_list_yq = ['预期描述：', problem.expect]
    desc_list.extend(desc_list_yq)

    # 问题结果 - HTML解析
    parser2 = MyHTMLParser()
    parser2.feed(problem.result)
    desc_list_2 = ['问题结果：']
    for strOrList in parser2.allStrList:
        if strOrList.startswith("data:image/png;base64"):
            base64_bytes = base64.b64decode(strOrList.replace("data:image/png;base64,", ""))
            # ~~~设置了固定宽度~~~
            desc_list_2.append(InlineImage(doc, io.BytesIO(base64_bytes), width=Mm(50)))
        else:
            desc_list_2.append(strOrList)
    desc_list.extend(desc_list_2)

    problem_dict['desciption'] = desc_list

    return problem_dict
