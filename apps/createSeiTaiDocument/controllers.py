# 测试运行时间
import time
from ninja_extra.controllers import api_controller, ControllerBase, route
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404
# 文档处理相关库
from docxtpl import DocxTemplate
# 导入docx进行文件“域”替换操作
from apps.createSeiTaiDocument.docXmlUtils import generate_temp_doc
# 自己的工具模块
from utils.chen_response import ChenResponse
# 模型模块
from apps.project.models import Project

# @api_controller("/create", tags=['生成产品文档接口'], auth=JWTAuth(), permissions=[IsAuthenticated])
@api_controller("/create", tags=['生成产品文档接口'])
class GenerateSeitaiController(ControllerBase):
    @route.get("/dgDocument", url_name="create-dgDocument")
    @transaction.atomic
    def create_dgDocument(self, id: int):
        # 获取项目Model
        project_obj = get_object_or_404(Project, id=id)
        # 生成大纲需要的基础变量context
        context = {'is_JD': False}
        if project_obj.report_type == '9':
            context['is_JD'] = True
        context['ident'] = project_obj.ident
        # TODO:暂时声明为公开
        context['sec_title'] = '公开'
        context['sec'] = '公开'
        context['name'] = project_obj.name
        context['duty_person'] = project_obj.duty_person
        if len(project_obj.member) > 0:
            context['member'] = project_obj.member[0]
        else:
            context['member'] = context['duty_person']
        context['entrust_unit'] = project_obj.entrust_unit

        result = generate_temp_doc('dg')
        if isinstance(result, dict):
            return ChenResponse(status=400, code=400, message=result.get('msg', 'dg未报出错误原因，反正在生成文档出错'))
        dg_replace_path, dg_seitai_final_path = result
        # behavior
        doc = DocxTemplate(dg_replace_path)
        start = time.time()
        doc.render(context)  # 耗时最长，TODO:异步任务处理？或前端等待？
        end = time.time()
        print('渲染耗时：', end - start)
        try:
            doc.save(dg_seitai_final_path)
            return ChenResponse(status=200, code=200, message="最终大纲生成成功！")
        except PermissionError as e:
            return ChenResponse(status=400, code=400, message="模版文件已打开，请关闭后再试，{0}".format(e))

    @route.get('/smDocument', url_name='create-smDocument')
    @transaction.atomic
    def create_smDocument(self, id: int):
        """生成最后说明文档"""
        # 获取项目对象
        project_obj = get_object_or_404(Project, id=id)
        # 首先第二层模版所需变量
        member = project_obj.member[0] if len(project_obj.member) > 0 else project_obj.duty_person
        context = {'name': project_obj.name, 'is_JD': False, 'ident': project_obj.ident, 'sec_title': "公开",
                   'duty_person': project_obj.duty_person, 'member': member}
        if project_obj.report_type == '9':
            context['is_JD'] = True
        # 提取第一轮测试中源代码 - 用户标识
        round_1 = project_obj.pField.filter(key='0').first()
        duty_so = round_1.rdField.filter(type='SO').first()
        if not duty_so:
            return ChenResponse(code=400, status=400, message="未找到第一轮测试中源代码被测件请添加")
        context['user_ident'] = duty_so.ref

        result = generate_temp_doc('sm')
        if isinstance(result, dict):
            return ChenResponse(code=400, status=400, message=result.get('msg', '无错误原因'))
        sm_to_tpl_file, sm_seitai_final_file = result

        doc = DocxTemplate(sm_to_tpl_file)
        start = time.time()
        doc.render(context)  # 耗时最长，TODO:异步任务处理？或前端等待？
        end = time.time()
        print('渲染耗时：', end - start)
        try:
            doc.save(sm_seitai_final_file)
            return ChenResponse(status=200, code=200, message="最终大纲生成成功！")
        except PermissionError as e:
            return ChenResponse(status=400, code=400, message="模版文件已打开，请关闭后再试，{0}".format(e))

    @route.get('/jlDocument', url_name='create-jlDocument')
    @transaction.atomic
    def create_jlDocument(self, id: int):
        project_obj = get_object_or_404(Project, id=id)
        # seitai文档所需变量
        ## 1.判断是否为JD
        member = project_obj.member[0] if len(project_obj.member) > 0 else project_obj.duty_person
        context = {'name': project_obj.name, 'ident': project_obj.ident, 'is_JD': False, 'sec_title': "公开",
                   'duty_person': project_obj.duty_person, 'member': member}
        if project_obj.report_type == '9':
            context['is_JD'] = True
        ## 2.判断被测件是否有需求文档/设计文档/手册文档
        for dut in project_obj.pdField.all():
            if dut.type == 'XQ':
                context['demandDocName'] = dut.name
            if dut.type == 'SJ':
                context['designDocName'] = dut.name
            # TODO:设置手册文档名称-暂时dut没有手册这个类型
            context['manualDocName'] = False
            context['isC'] = True if '1' in project_obj.language else False
            context['isCplus'] = True if '2' in project_obj.language else False

        result = generate_temp_doc('jl')
        if isinstance(result, dict):
            return ChenResponse(code=400, status=400, message=result.get('msg', '无错误原因'))
        jl_to_tpl_file, jl_seitai_final_file = result

        doc = DocxTemplate(jl_to_tpl_file)
        start = time.time()
        doc.render(context)  # 耗时最长，TODO:异步任务处理？或前端等待？
        end = time.time()
        print('渲染耗时：', end - start)
        try:
            doc.save(jl_seitai_final_file)
            return ChenResponse(status=200, code=200, message="最终大纲生成成功！")
        except PermissionError as e:
            return ChenResponse(status=400, code=400, message="模版文件已打开，请关闭后再试，{0}".format(e))

    @route.get('/bgDocument', url_name='create-bgDocument')
    @transaction.atomic
    def create_bgDocument(self, id: int):
        """生成最后的报告文档"""
        project_obj = get_object_or_404(Project, id=id)
        # seitai文档所需变量
        ## 1.判断是否为JD
        member = project_obj.member[0] if len(project_obj.member) > 0 else project_obj.duty_person
        context = {'name': project_obj.name, 'ident': project_obj.ident, 'is_JD': False, 'sec_title': "公开",
                   'duty_person': project_obj.duty_person, 'member': member}
        if project_obj.report_type == '9':
            context['is_JD'] = True
        context['entrust_unit'] = project_obj.entrust_unit

        result = generate_temp_doc('bg')
        if isinstance(result, dict):
            return ChenResponse(status=400, code=400, message=result.get('msg', 'bg未报出错误原因，反正在生成文档出错'))
        bg_replace_path, bg_seitai_final_path = result
        # behavior
        doc = DocxTemplate(bg_replace_path)
        start = time.time()
        doc.render(context)  # 耗时最长，TODO:异步任务处理？或前端等待？
        end = time.time()
        print('渲染耗时：', end - start)
        try:
            doc.save(bg_seitai_final_path)
            return ChenResponse(status=200, code=200, message="最终报告生成成功！")
        except PermissionError as e:
            return ChenResponse(status=400, code=400, message="模版文件已打开，请关闭后再试，{0}".format(e))

    @route.get('/wtdDocument', url_name='create-wtdDocument')
    @transaction.atomic
    def create_wtdDocument(self, id: int):
        """生成最后的问题单"""
        project_obj = get_object_or_404(Project, id=id)
        # seitai文档所需变量
        member = project_obj.member[0] if len(project_obj.member) > 0 else project_obj.duty_person
        context = {'name': project_obj.name, 'ident': project_obj.ident, 'sec_title': "公开",
                   'duty_person': project_obj.duty_person, 'member': member}

        result = generate_temp_doc('wtd')
        if isinstance(result, dict):
            return ChenResponse(status=400, code=400, message=result.get('msg', 'wtd未报出错误原因，反正在生成文档出错'))
        wtd_replace_path, wtd_seitai_final_path = result
        # behavior
        doc = DocxTemplate(wtd_replace_path)
        start = time.time()
        doc.render(context)  # 耗时最长，TODO:异步任务处理？或前端等待？
        end = time.time()
        print('渲染耗时：', end - start)
        try:
            doc.save(wtd_seitai_final_path)
            return ChenResponse(status=200, code=200, message="问题单生成成功！")
        except PermissionError as e:
            return ChenResponse(status=400, code=400, message="模版文件已打开，请关闭后再试，{0}".format(e))
