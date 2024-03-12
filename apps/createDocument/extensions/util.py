from pathlib import Path
from docx import Document
from docxtpl import DocxTemplate
from docx.table import Table
from utils.chen_response import ChenResponse

def merge_all_cell(table: Table) -> None:
    """逐个找第二列和第三列单元格的text，如果一致则合并"""
    col_list = [table.columns[1], table.columns[2]]
    # 合并第二列相同的单元格
    for col_right in col_list:
        index = 0
        temp_text = ""
        for cell in col_right.cells:
            if index == 0:
                temp_text = cell.text
            else:
                if cell.text == temp_text:
                    text_temp = cell.text
                    ce = cell.merge(col_right.cells[index - 1])
                    ce.text = text_temp
                else:
                    temp_text = cell.text
            index += 1

# 生成文档的工具函数 -sm
def create_sm_docx(template_name: str, context: dict) -> ChenResponse:
    input_path = Path.cwd() / 'media' / 'form_template' / 'sm' / template_name
    doc = DocxTemplate(input_path)
    doc.render(context)
    try:
        doc.save(Path.cwd() / "media/output_dir/sm" / template_name)
        return ChenResponse(status=200, code=200, message="文档生成成功！")
    except PermissionError as e:
        return ChenResponse(status=400, code=400, message="模版文件已打开，请关闭后再试，{0}".format(e))

# 生成文档的工具函数 -dg
def create_dg_docx(template_name: str, context: dict) -> ChenResponse:
    input_path = Path.cwd() / 'media' / 'form_template' / 'dg' / template_name
    doc = DocxTemplate(input_path)
    doc.render(context)
    try:
        doc.save(Path.cwd() / "media/output_dir" / template_name)
        return ChenResponse(status=200, code=200, message="文档生成成功！")
    except PermissionError as e:
        return ChenResponse(status=400, code=400, message="模版文件已打开，请关闭后再试，{0}".format(e))