import base64
import io
from datetime import datetime, timedelta
from ninja_extra import ControllerBase, api_controller, route
from ninja_extra.permissions import IsAuthenticated
from ninja_jwt.authentication import JWTAuth
from django.db import transaction
from django.db.models import Q
from docxtpl import DocxTemplate, RichText, InlineImage
from docx.shared import Mm
from pathlib import Path
from utils.chen_response import ChenResponse
# 导入数据库ORM
from apps.project.models import TestDemand, TestDemandContent, Project, Contact, Design, Abbreviation
from apps.dict.models import Dict, DictItem
# 导入工具函数
from utils.util import get_str_dict, get_list_dict, get_testType, get_ident
from utils.chapter_tools.csx_chapter import create_csx_chapter_dict
from utils.util import MyHTMLParser, MyHTMLParser_p
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from apps.createDocument.extensions.util import create_dg_docx

# @api_controller("/generate", tags=['生成大纲文档'], auth=JWTAuth(), permissions=[IsAuthenticated])
@api_controller("/generate", tags=['生成大纲文档'])
class GenerateControllerDG(ControllerBase):
    @route.get("/create/testdemand", url_name="create-testdemand")
    @transaction.atomic
    def create_testdemand(self, id: int):
        """目前生成第一轮测试项"""
        tplTestDemandGenerate_path = Path.cwd() / "media" / "form_template" / "dg" / "测试项及方法.docx"
        doc = DocxTemplate(tplTestDemandGenerate_path)
        # 获取指定的项目对象
        project_qs = get_object_or_404(Project, id=id)
        # 先查询dict字典，查出总共有多少个testType
        test_type_len = Dict.objects.get(code='testType').dictItem.count()
        type_number_list = [i for i in range(1, test_type_len + 1)]
        list_list = [[] for j in range(1, test_type_len + 1)]
        # 查出第一轮所有testdemand
        project_round_one = project_qs.pField.filter(key=0).first()
        testDemand_qs = project_round_one.rtField.all()
        for single_qs in testDemand_qs:
            type_index = type_number_list.index(int(single_qs.testType))
            # 先查询其testDemandContent信息
            content_list = []
            for (index, content) in enumerate(single_qs.testQField.all()):
                content_dict = {
                    "index": index + 1,
                    "testXuQiu": content.testXuQiu,
                    "testYuQi": content.testYuQi
                }
                content_list.append(content_dict)
            # 查询测试项中testMethod
            testmethod_str = ''
            for dict_item_qs in Dict.objects.get(code="testMethod").dictItem.all():
                for tm_item in single_qs.testMethod:
                    if tm_item == dict_item_qs.key:
                        testmethod_str += dict_item_qs.title + " "
            # 解析富文本HTML
            parser = MyHTMLParser()
            parser.feed(single_qs.design.description)
            desc_list = []
            for strOrList in parser.allStrList:
                if strOrList.startswith("data:image/png;base64"):
                    base64_bytes = base64.b64decode(strOrList.replace("data:image/png;base64,", ""))
                    # ~~~设置了固定宽度~~~
                    desc_list.append(InlineImage(doc, io.BytesIO(base64_bytes), width=Mm(115)))
                else:
                    desc_list.append(strOrList)
            # 查询关联design以及普通design
            doc_list = [{'dut_name': single_qs.dut.name, 'design_chapter': single_qs.design.chapter,
                         'design_name': single_qs.design.name}]
            for relate_design in single_qs.otherDesign.all():
                ddict = {'dut_name': relate_design.dut.name, 'design_chapter': relate_design.chapter,
                         'design_name': relate_design.name}
                doc_list.append(ddict)

            # 组装单个测试项
            testdemand_dict = {
                "name": single_qs.name,
                "ident": get_ident(single_qs),
                "priority": get_str_dict(single_qs.priority, "priority"),
                "doc_list": doc_list,
                "design_description": desc_list,
                "test_demand_content": content_list,
                "testMethod": testmethod_str,
                "adequacy": single_qs.adequacy.replace("\n", "\a"),
                "termination": single_qs.termination.replace("\n", "\a"),
                "premise": single_qs.premise.replace("\n", "\a"),
            }
            list_list[type_index].append(testdemand_dict)

        # 定义渲染context字典
        context = {
            "project_name": "测试项目!!!!"
        }
        output_list = []

        for (index, li) in enumerate(list_list):
            qs = Dict.objects.get(code="testType").dictItem.get(key=str(index + 1))
            context_str = qs.title
            sort = qs.sort
            table = {
                "type": context_str,
                "item": li,
                "sort": sort
            }
            output_list.append(table)
        # 排序
        output_list = sorted(output_list, key=(lambda x: x["sort"]))
        context["data"] = output_list
        doc.render(context)
        try:
            doc.save(Path.cwd() / "media/output_dir" / "测试项及方法.docx")
            return ChenResponse(status=200, code=200, message="文档生成成功！")
        except PermissionError as e:
            return ChenResponse(status=400, code=400, message="模版文件已打开，请关闭后再试，{0}".format(e))

    @route.get("/create/yiju", url_name='create-yiju')
    @transaction.atomic
    def create_yiju(self, id: int):
        # 先找出所属项目
        project_qs = get_object_or_404(Project, id=id)
        # 找出该项目的真实依据文件qs
        yiju_list = get_list_dict('standard', project_qs.standard)
        context = {
            'std_documents': yiju_list
        }
        return create_dg_docx('标准依据文件.docx', context)

    @route.get("/create/techyiju", url_name='create-techyiju')
    @transaction.atomic
    def create_techyiju(self, id: int):
        # 找出所属项目
        project_qs = get_object_or_404(Project, id=id)
        # 根据项目找出被测件
        duties_qs = project_qs.pdField.filter(Q(type='XQ') | Q(type='SJ') | Q(type='XY'))
        # 先定义个字典
        std_documents = []
        for duty in duties_qs:
            one_duty = {'doc_name': duty.name, 'ident_version': duty.ref + '-' + duty.version,
                        'publish_date': duty.release_date, 'source': duty.release_union}
            std_documents.append(one_duty)

        # 生成二级文档
        context = {
            'std_documents': std_documents
        }
        return create_dg_docx('技术依据文件.docx', context)

    @route.get("/create/contact", url_name='create-contact')
    @transaction.atomic
    def create_contact(self, id: int):
        # 先找出所属项目
        project_qs = get_object_or_404(Project, id=id)
        contact_dict = model_to_dict(project_qs,
                                     fields=['entrust_unit', 'entrust_contact', 'entrust_contact_phone', 'dev_unit',
                                             'dev_contact', 'dev_contact_phone', 'test_unit', 'test_contact',
                                             'test_contact_phone'])
        # 根据entrust_unit、dev_unit、test_unit查找Contact中地址信息
        entrust_addr = Contact.objects.get(name=contact_dict['entrust_unit']).addr
        dev_addr = Contact.objects.get(name=contact_dict['dev_unit']).addr
        test_addr = Contact.objects.get(name=contact_dict['test_unit']).addr
        contact_dict['entrust_addr'] = entrust_addr
        contact_dict['dev_addr'] = dev_addr
        contact_dict['test_addr'] = test_addr
        context = {
            'datas': contact_dict
        }
        return create_dg_docx('联系人和方式.docx', context)

    # 生成测评时间和地点
    @route.get('/create/timeaddress', url_name='create-timeaddress')
    @transaction.atomic
    def create_timeaddress(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        # 获取项目开始日期
        beginTime = project_qs.beginTime
        beginTime_strf = beginTime.strftime("%Y%m%d")
        # 生成大纲编制开始和结束时间
        dgCompileStart = (beginTime + timedelta(days=1)).strftime("%Y%m%d")
        dgCompileEnd = (beginTime + timedelta(days=6)).strftime("%Y%m%d")
        # 测评设计与实现开始和结束时间
        designStart = (beginTime + timedelta(days=7)).strftime("%Y%m%d")
        designEnd = (beginTime + timedelta(days=13)).strftime("%Y%m%d")
        # 生成文档
        begin_time = project_qs.beginTime
        context = {
            'year': begin_time.year,
            'month': begin_time.month,
            'day': begin_time.day,
            'beginTime_strf': beginTime_strf,
            'dgCompileStart': dgCompileStart,
            'dgCompileEnd': dgCompileEnd,
            'designStart': designStart,
            'designEnd': designEnd,
        }
        return create_dg_docx('测评时间和地点.docx', context)

    # 生成被测软件功能-根据需求表生成
    @route.get('/create/funcList', url_name='create-funcList')
    @transaction.atomic
    def create_funcList(self, id: int):
        # 获取context数据
        project_qs = get_object_or_404(Project, id=id)
        funcList = []
        # 只取第一轮的设计需求，且只能是非其他
        for designDemand in project_qs.psField.filter(~Q(demandType='6'), round__key='0'):
            func = {}
            # 如果需求类型字典值为1
            if designDemand.demandType == '1':
                func['func_name'] = designDemand.name
                parser = MyHTMLParser_p()
                parser.feed(designDemand.description)
                p_list = parser.allStrList
                # 拼接具体内容，如果有多项则换行
                func['func_description'] = '\n'.join(p_list)
                funcList.append(func)
        context = {
            'project_name': project_qs.name,
            'funcList': funcList
        }
        return create_dg_docx('被测软件功能.docx', context)

    # 生成被测软件接口-根据需求类型为接口的生成
    @route.get('/create/interfaceList', url_name='create-interfaceList')
    @transaction.atomic
    def create_interfaceList(self, id: int):
        pass

    # 生成测评对象 - 包括大纲、说明
    @route.get('/create/softComposition', url_name='create-softComposition')
    @transaction.atomic
    def create_softComposition(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        project_name = project_qs.name
        context = {
            'project_name': project_name
        }
        return create_dg_docx('测评对象.docx', context)

    # 生成被测软件接口章节
    @route.get('/create/interface', url_name='create-interface')
    def create_interface(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        project_name = project_qs.name
        interfaceNameList = []
        # 查询接口列表
        iters = project_qs.psField.filter(demandType=3)
        iters_length = len(iters)
        index = 0
        for inter in iters:
            interfaceNameList.append(inter.name)
            index += 1
            if index < iters_length:
                interfaceNameList.append('、')
        # 渲染文档
        context = {
            'project_name': project_name,
            'iters': interfaceNameList,
            'iter_list': iters,
        }
        ### TODO:生成接口列表
        return create_dg_docx('被测软件接口.docx', context)

    # 生成被测软件性能章节
    @route.get('/create/performance', url_name='create-performance')
    def create_performance(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        # 查询性能的design
        design_qs = project_qs.psField.filter(demandType=2)
        # 渲染列表
        performance_list = []
        # 实例化HTML解析器
        index = 0
        for design_one in design_qs:
            html_parser = MyHTMLParser_p()
            html_parser.feed(design_one.description)
            index += 1
            performance_list.append(f"{index}、" + "\a".join(html_parser.allStrList))
        context = {
            'performance_list': performance_list
        }
        return create_dg_docx('被测软件性能.docx', context)

    # 生成软硬件环境
    @route.get('/create/environment', url_name='create-environment')
    def create_environment(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        context = {}
        return create_dg_docx("软硬件环境.docx", context)

    # 生成被测软件-基本信息
    @route.get('/create/baseInformation', url_name='create-baseInformation')
    def create_information(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        security = get_str_dict(project_qs.security_level, 'security_level')
        languages = get_list_dict('language', project_qs.language)
        runtime = get_str_dict(project_qs.runtime, 'runtime')
        devplant = get_str_dict(project_qs.devplant, 'devplant')
        language_list = []
        for language in languages:
            language_list.append(language.get('ident_version'))
        # 版本先找第一轮
        project_round = project_qs.pField.filter(key=0).first()
        first_round_SO = project_round.rdField.filter(type='SO').first()
        version = first_round_SO.version
        line_count = first_round_SO.total_code_line
        dev_unit = project_qs.dev_unit
        # 渲染上下文
        context = {
            'project_name': project_qs.name,
            'security_level': security,
            'language': "\a".join(language_list),
            'version': version,
            'line_count': line_count,
            'recv_date': project_qs.beginTime.strftime("%Y-%m-%d"),
            'dev_unit': dev_unit,
            'soft_type': project_qs.get_soft_type_display(),
            'runtime': runtime,
            'devplant': devplant
        }
        return create_dg_docx('被测软件基本信息.docx', context)

    # 生成测试总体要求
    @route.get('/create/requirement', url_name='create-requirement')
    def create_requirement(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        # 查询首轮被测件
        round1 = project_qs.pField.filter(key='0').first()
        dut_qs = round1.rdField.filter(Q(type='XQ') | Q(type='XY') | Q(type='SJ'))
        dut_str_list = []
        for dut in dut_qs:
            dut_str_list.append(dut.name)
        security_boolean = True if int(project_qs.security_level) <= 2 else False
        # 查看测试类型-TODO:暂未思考出解决方案

        context = {
            'project_name': project_qs.name,
            'dut_str': '、'.join(dut_str_list),
            'security_boolean': security_boolean,
        }
        return create_dg_docx('测试总体要求.docx', context)

    # 生成-测试内容充分性及测试方法有效性
    @route.get('/create/adequacy_effectiveness', url_name='create-adequacy_effectiveness')
    def create_adequacy_effectiveness(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        # 统计测试种类数量-只统计第一轮测试
        project_round_one = project_qs.pField.filter(key=0).first()
        if project_round_one:
            pass
        else:
            return ChenResponse(status=400, code=400, message="未找到首轮测试信息!")
        # 通过字典获取-测试方法
        type_dict = {}  # key为测试类型，value为数量
        testDemands = project_round_one.rtField.all()
        for testDemand in testDemands:
            # 获取每个测试项测试类型
            test_type = get_list_dict('testType', testDemand.testType)[0].get('ident_version')
            # 如果字典没有该key，则创建并value=1
            if not test_type in type_dict:
                type_dict[test_type] = 1
            else:
                type_dict[test_type] += 1
        length = len(type_dict)
        type_str_list = []
        for key, value in type_dict.items():
            type_str_list.append(f"{key}{value}项")
        context = {
            'project_name': project_qs.name,
            'length': length,
            'type_str': "、".join(type_str_list),
        }
        return create_dg_docx('测试内容充分性及测试方法有效性分析.docx', context)

    # 生成-测评项目组组成和分工
    @route.get('/create/group', url_name='create_group')
    def create_group(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        context = {
            'duty_person': project_qs.duty_person,
            'member_str': "、".join(project_qs.member),
            'quality_person': project_qs.quality_person,
            'vise_person': project_qs.vise_person,
            'config_person': project_qs.config_person,
            'dev_unit': project_qs.dev_unit,
        }
        return create_dg_docx('测评组织及任务分工.docx', context)

    # 生成-测评条件保障
    @route.get('/create/guarantee', url_name='create-guarantee')
    def create_guarantee(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        context = {
            'project': project_qs
        }
        return create_dg_docx('测评条件保障.docx', context)

    # 生成-缩略语
    @route.get('/create/abbreviation', url_name='create-abbreviation')
    def create_abbreviation(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        abbreviations = []
        for abbr in project_qs.abbreviation:
            abbr_dict = {'title': abbr, 'des': Abbreviation.objects.filter(title=abbr).first().des}
            abbreviations.append(abbr_dict)

        context = {
            'abbreviations': abbreviations
        }

        return create_dg_docx('缩略语.docx', context)

    # 生成研制总要求-测试项追踪关系表
    @route.get('/create/yzComparison', url_name='create-yzComparison')
    def create_yzComparison(self, id: int):
        """目前追踪需求项的章节号是硬编码，按6.2章节起步，6.2.1~x.x.x依次排序"""
        # 规定测试项的章节号开头
        test_item_prefix = '6.2'
        # 计算有多少种testType - '文档审查'/'功能测试' ->
        # 形成一个数组['1','2','3','4','9']后面用来判断测试项的章节号
        project_qs = get_object_or_404(Project, id=id)
        design_list = []  # 先按照design的思路进行追踪
        # 判断是否为鉴定测评，有则生成该表
        if project_qs.report_type == '9':
            project_round_one = project_qs.pField.filter(key=0).first()
            testType_list, last_chapter_items = create_csx_chapter_dict(project_round_one)
            # 找出第一轮的研总
            yz_dut = project_round_one.rdField.filter(type='YZ').first()
            if yz_dut:
                # 查询出验证所有design
                yz_designs = yz_dut.rsField.all()
                # 遍历所有研总的design
                for design in yz_designs:
                    design_dict = {'name': design.name, 'chapter': design.chapter, 'test_demand': []}
                    # 获取一个design的所有测试项
                    test_items = design.dtField.all()
                    for test_item in test_items:
                        key_index = int(test_item.key.split("-")[-1]) + 1
                        test_index = str(key_index).rjust(3, '0')
                        reveal_ident = "_".join(
                            ["XQ", get_testType(test_item.testType, "testType"), test_item.ident, test_index])
                        # 查字典方式确认章节号最后一位
                        test_item_last_chapter = last_chapter_items[test_item.testType].index(test_item.key) + 1
                        test_chapter = ".".join([test_item_prefix, str(testType_list.index(test_item.testType) + 1),
                                                 str(test_item_last_chapter)])
                        test_item_dict = {'name': test_item.name, 'chapter': test_chapter, 'ident': reveal_ident}
                        design_dict['test_demand'].append(test_item_dict)
                    design_list.append(design_dict)
                context = {
                    'design_list': design_list
                }
                return create_dg_docx('研制总要求追踪表.docx', context)

    # 生成需求规格说明-测试项追踪关系表
    @route.get('/create/xqComparison', url_name='create-xqComparison')
    def create_xqComparison(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        test_item_prefix = '6.2'
        design_list = []
        project_round_one = project_qs.pField.filter(key=0).first()
        if project_round_one:
            testType_list, last_chapter_items = create_csx_chapter_dict(project_round_one)
            # 找出第一轮的被测件为'XQ'
            xq_dut = project_round_one.rdField.filter(type='XQ').first()
            # 找出第一轮被测件为'SO'，其中的测试项
            so_dut = project_round_one.rdField.filter(type='SO').first()
            if so_dut:
                so_designs = so_dut.rsField.all()
                for design in so_designs:
                    design_dict = {'name': "/", 'chapter': "/", 'test_demand': []}
                    # 获取一个design的所有测试项
                    test_items = []
                    test_items.extend(design.dtField.all())
                    test_items.extend(design.odField.all())

                    for test_item in test_items:
                        # 只对文档审查、静态分析、代码走查、代码审查进行处理
                        if test_item.testType in ['8', '15', '3', '2']:
                            key_index = int(test_item.key.split("-")[-1]) + 1
                            test_index = str(key_index).rjust(3, '0')
                            reveal_ident = "_".join(
                                ["XQ", get_testType(test_item.testType, "testType"), test_item.ident, test_index])
                            # 查字典方式确认章节号最后一位
                            test_item_last_chapter = last_chapter_items[test_item.testType].index(test_item.key) + 1
                            test_chapter = ".".join([test_item_prefix, str(testType_list.index(test_item.testType) + 1),
                                                     str(test_item_last_chapter)])
                            test_item_dict = {'name': test_item.name, 'chapter': test_chapter, 'ident': reveal_ident}
                            design_dict['test_demand'].append(test_item_dict)
                    design_list.append(design_dict)

            if xq_dut:
                xq_designs = xq_dut.rsField.all()
                for design in xq_designs:
                    design_dict = {'name': design.name, 'chapter': design.chapter, 'test_demand': []}
                    # 获取一个design的所有测试项
                    test_items = []
                    test_items.extend(design.dtField.all())
                    test_items.extend(design.odField.all())

                    for test_item in test_items:
                        key_index = int(test_item.key.split("-")[-1]) + 1
                        test_index = str(key_index).rjust(3, '0')
                        reveal_ident = "_".join(
                            ["XQ", get_testType(test_item.testType, "testType"), test_item.ident, test_index])
                        # 查字典方式确认章节号最后一位
                        test_item_last_chapter = last_chapter_items[test_item.testType].index(test_item.key) + 1
                        test_chapter = ".".join([test_item_prefix, str(testType_list.index(test_item.testType) + 1),
                                                 str(test_item_last_chapter)])
                        test_item_dict = {'name': test_item.name, 'chapter': test_chapter, 'ident': reveal_ident}
                        design_dict['test_demand'].append(test_item_dict)

                    design_list.append(design_dict)
                context = {
                    'design_list': design_list
                }
                return create_dg_docx('需求规格说明追踪表.docx', context)

    # 生成测试项-需求规格说明关系表【反向】
    @route.get('/create/fanXqComparison', url_name='create-fanXqComparison')
    def create_fanXqComparison(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        test_item_prefix = '6.2'
        # 取出第一轮所有测试项的章节处理列表和字典
        project_round_one = project_qs.pField.filter(key=0).first()
        testType_list, last_chapter_items = create_csx_chapter_dict(project_round_one)
        # 查询第一轮所有测试项
        test_items = []
        test_items.extend(project_round_one.rtField.all())
        # 最后渲染列表
        items_list = []
        for test_item in test_items:
            # 第二个处理被测件为"XQ"，第二个处理被测件为'SO'，并且为测试项testType为['8', '15', '3', '2']的
            if test_item.dut.type == 'XQ' or (test_item.dut.type == 'SO' and test_item.testType in ['8', '15', '3',
                                                                                                    '2']):
                key_index = int(test_item.key.split("-")[-1]) + 1
                test_index = str(key_index).rjust(3, '0')
                reveal_ident = "_".join(
                    ["XQ", get_testType(test_item.testType, "testType"), test_item.ident, test_index])
                # 查字典方式确认章节号最后一位
                test_item_last_chapter = last_chapter_items[test_item.testType].index(test_item.key) + 1
                test_chapter = ".".join([test_item_prefix, str(testType_list.index(test_item.testType) + 1),
                                         str(test_item_last_chapter)])
                # 如果是SO里面的
                if test_item.testType in ['8', '15', '3', '2'] and test_item.dut.type == 'SO':
                    test_item_dict = {'name': test_item.name, 'chapter': test_chapter, 'ident': reveal_ident,
                                      'design': {
                                          'name': "/", 'chapter': "/"
                                      }}
                else:
                    test_item_dict = {'name': test_item.name, 'chapter': test_chapter, 'ident': reveal_ident,
                                      'design': {
                                          'name': test_item.design.name, 'chapter': test_item.design.chapter
                                      }}
                items_list.append(test_item_dict)
        context = {
            'items_list': items_list,
        }
        return create_dg_docx('反向需求规格追踪表.docx', context)

    # 生成代码质量度量分析表
    @route.get('/create/codeQuality', url_name='create-codeQuality')
    def create_codeQuality(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        project_round_one = project_qs.pField.filter(key=0).first()
        context = {}
        context.update({'project_name': project_qs.name})
        if project_round_one:
            source_dut = project_round_one.rdField.filter(type='SO').first()
            if source_dut:
                context.update({'version': source_dut.version})
                context.update({'size': source_dut.total_line})
                context.update({'total_code_line': source_dut.total_code_line})
                context.update({'comment_line': source_dut.total_comment_line})
                context.update({'black_line': source_dut.black_line})
            else:
                return ChenResponse(message='未找到源代码被测件', code=400)
        return create_dg_docx('代码质量度量分析表.docx', context)

    # 生成-主要战技术指标
    @route.get('/create/mainTech', url_name='create-mainTech')
    @transaction.atomic
    def create_mainTech(self, id: int):
        project_qs = get_object_or_404(Project, id=id)
        # 首先要把研制总要求搜索出来
        if project_qs.report_type == '9':
            project_round_one = project_qs.pField.filter(key=0).first()
            # 找出第一轮的研总
            yz_dut = project_round_one.rdField.filter(type='YZ').first()
            if yz_dut:
                # 查询出验证所有design
                yz_designs = yz_dut.rsField.all()
                # 定义渲染变量列表-以研总的测试需求为单个变量
                data_list = []
                # 然后检索出所有研总对应的测试需求
                for design in yz_designs:
                    # 这里每个设计需求构造一个对象
                    parser = MyHTMLParser_p()
                    parser.feed(design.description)
                    p_list = parser.allStrList
                    design_dict: dict = {'chapter': design.chapter, 'description': '\a'.join(p_list), 'testDemand': []}
                    # 这里需要判断测试项是否属于需求规格说明文档，并且获取该dut信息
                    for demand in design.odField.all():
                        if demand.dut.type == 'XQ':
                            parser_one = MyHTMLParser_p()
                            parser_one.feed(design.description)
                            p_one_list = parser_one.allStrList
                            xq_design_dict = {'chapter': demand.design.chapter, 'description': '\a'.join(p_one_list)}
                            design_dict['testDemand'].append(xq_design_dict)
                    data_list.append(design_dict)
                context = {'data_list': data_list}
                return create_dg_docx('主要战技指标.docx', context)
