"""该模块主要自动生成静态分析、代码审查以及文档审查的设计需求、测试项、用例"""
from apps.project.models import Project, Dut, Design, TestDemand, TestDemandContent, Case, CaseStep

def auto_create_jt_and_dm(user_name: str, dut_qs: Dut, project_obj: Project):
    """传入源代码dut以及测试人员名称username，自动在dut下面生成静态分析和代码审查设计需求、测试项、用例"""
    # 先查询dut_qs下面有多少design，以便写里面的key
    design_index = dut_qs.rsField.count()
    # 1.1.自动创建design静态分析
    jt_design_create_dict = {
        'ident': 'JTFX',
        'name': '静态分析',
        'demandType': '6',
        'description': "根据相关要求，利用静态分析工具对被测软件全部源程序进行控制流分析、"
                       "数据流分析进行分析，并统计软件质量度量信息，给出软件源代码检查结果",
        'title': '静态分析',
        'key': ''.join([dut_qs.key, '-', str(design_index)]),
        'level': '2',
        'chapter': '/',
        'project': project_obj,
        'round': dut_qs.round,
        'dut': dut_qs
    }
    design_index += 1
    new_design_jt: Design = Design.objects.create(**jt_design_create_dict)
    # 1.1.1.自动创建demand静态分析
    jt_demand_create_dict = {
        'ident': 'JTFX',
        'name': '静态分析',
        'adequacy': '对软件全部源程序进行进行质量度量、控制流分析、数据流分析的静态统计信息分析',
        'priority': '2',
        'testType': '15',
        'testMethod': ["3"],
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
                                             '对控制流、数据流进行分析，验证软件是否满足控制流和数据流要求，'
                                             '并依据质量特性需求统计质量度量信息',
                                     condition='',
                                     operation='使用LDRA '
                                               'TestBed软件和Klocwork软件工具对被测软件全部源'
                                               '程序进行静态分析，依据附录的审查单对源程序进行检查。'
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
        'description': "根据相关要求及软件文档开展针对软件程序代码的代码审查",
        'title': '代码审查',
        'key': ''.join([dut_qs.key, '-', str(design_index)]),
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
        'testMethod': ["3"],
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
        condition='',
        operation='人工审查及借助工具辅助分析的方式',
        observe='和依据附录代码审查单范围内的源代码开展四个方面的审查：\a'
                '1）编程准则检查：依据编程准则的要求，对程序的编码与编程准则进行符合性检查；\a'
                '2）代码流程审查：审查程序代码的条件判别、控制流程、数据处理等满足设计要求；\a'
                '3）软件结构审查：依据设计文档，审查程序代码的结构设计的合理性，包括程序结构设计和数据结构设计；\a'
                '4）需求实现审查：依据需求文档及其他相关资料，审查程序代码的需求层的功能实现是否正确',
        expect=''
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

def auto_create_wd(user_name: str, dut_qs: Dut, project_obj: Project):
    """传入用户名、在dut下创建、项目对象，自动创建文档审查的设计需求、测试项、测试用例"""
    # 先查询dut_qs下有多少desgin，然后设置key
    design_index = dut_qs.rsField.count()
    # 1.1.自动创建文档审查design
    wd_design_create_dict = {
        'ident': 'WDSC',
        'name': '文档审查',
        'demandType': '6',
        'description': "依据相关要求，逐项检查被测文档的完整性、一致性和准确性是否满足要求",
        'title': '文档审查',
        'key': ''.join([dut_qs.key, '-', str(design_index)]),
        'level': '2',
        'chapter': '/',
        'project': project_obj,
        'round': dut_qs.round,
        'dut': dut_qs
    }
    new_wd_design_obj: Design = Design.objects.create(**wd_design_create_dict)
    # 1.1.1.自动创建demand静态分析
    wd_demand_create_dict = {
        'ident': 'WDSC',
        'name': '文档审查',
        'adequacy': '对所有被测软件文档按照文档检查单逐项进行审查',
        'priority': '1',
        'testType': '8',
        'testMethod': ["3"],
        'title': '文档审查',
        'key': ''.join([new_wd_design_obj.key, '-', '0']),
        'level': '3',
        'project': project_obj,
        'round': new_wd_design_obj.round,
        'dut': new_wd_design_obj.dut,
        'design': new_wd_design_obj,
    }
    new_wd_demand_obj = TestDemand.objects.create(**wd_demand_create_dict)
    TestDemandContent.objects.create(testDemand=new_wd_demand_obj, subName='文档审查',
                                     subDesc='本软件文档审查包括内容如下：\a'
                                             '1）软件需求规格说明\a'
                                             '2）软件设计文档\a'
                                             '3）软件接口需求规格说明\a'
                                             '4）软件接口设计说明\a'
                                             '5）软件用户手册',
                                     condition='',
                                     operation='测试人员人工阅读文档，依据文档检查单对软件文档进行审查，'
                                               '文档审查工作内容包括：\a'
                                               '1）审查软件文档内容是否完整；\a'
                                               '2）审查软件文档描述是否正确；\a'
                                               '3）审查软件文档格式是否规范；\a'
                                               '4）审查软件文档是否文文一致\a'
                                               '按照附录的需求规格说明审查单，对被测软件的需求规格说明进行审查；\a'
                                               '按照附录的软件设计文档审查单，对被测软件的设计说明文档进行审查；\a'
                                               '按照附录的用户手册审查单，对被测软件的用户手册进行审查', )
    new_wd_case_obj = Case.objects.create(
        ident='WDSC',
        name='文档审查',
        initialization='开发方已提交被测文档',
        premise='提交的文档出自委托方受控库，是委托方正式签署外发的',
        summarize='测试人员阅读文档，依据文档检查单对软件文档进行审查，审查文档内容是否完整、'
                  '文档描述是否准确、文档格式是否规范、文档是否文文一致',
        designPerson=user_name,
        testPerson=user_name,
        monitorPerson=user_name,
        project=project_obj,
        isLeaf=True,
        round=new_wd_demand_obj.round,
        dut=new_wd_demand_obj.dut,
        design=new_wd_demand_obj.design,
        test=new_wd_demand_obj,
        title='文档审查',
        key=''.join([new_wd_demand_obj.key, '-', '0']),
        level='4'
    )
    CaseStep.objects.create(case=new_wd_case_obj,
                            operation='按照测试需求中文档齐套性检查单检查需求类、设计类、用户类、测试类文档是否齐套',
                            expect='文档齐套性检查单全部通过，软件文档齐套',
                            result='文档齐套性检查单全部通过，软件文档齐套', )
    CaseStep.objects.create(case=new_wd_case_obj,
                            operation='按照测试需求中文档需求规格说明、设计文档等审查单，对相关文档进行审查',
                            expect='文档满足完整性、准确性、规范性和一致性的要求',
                            result='文档检查单全部审查通过，文档内容完整、文档描述准确、'
                                   '文档格式规范、文档文文一致', )
