from copy import deepcopy
from django.shortcuts import get_object_or_404
from apps.project.models import Project

def demand_copy_to_design(project_id: int, demand_key: str, design_id: int, depth: bool = False):
    """注意传入项目id，测试项是key，设计需求是id"""
    project_qs = get_object_or_404(Project, id=project_id)
    design = project_qs.psField.filter(id=design_id).first()
    demand = project_qs.ptField.filter(key=demand_key).first()
    # 1.这里先要根据老的demand取出其步骤，并深度复制
    origin_demand = deepcopy(demand)
    demand.id = None
    demand.title = '(复制)' + demand.title
    demand.name = '(复制)' + demand.name
    demand.dut = design.dut
    demand.round = design.round
    demand.design = design
    demand.ident += '(复制)'
    # 先查询目标design下面有多少个demand，然后key+1
    demand.key = "".join([design.key, '-', str(design.dtField.count())])
    demand.save()
    for sub in origin_demand.testQField.all():
        sub.id = None
        sub.testDemand = demand
        sub.save()
    # 2.如果depth=True，则复制用例过去
    if depth:
        for case in origin_demand.tcField.all():
            origin_case = deepcopy(case)
            case.id = None
            case.round = demand.round
            case.dut = demand.dut
            case.design = demand.design
            case.test = demand
            # 处理新case的key
            case_key_lastkey = case.key.split("-")[-1]
            case.key = "".join([demand.key, '-', case_key_lastkey])
            case.save()
            for case_step in origin_case.step.all():
                case_step.id = None
                case_step.case = case
                case_step.save()
    return demand.key
