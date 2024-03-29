import numpy as np
from ninja_extra import api_controller, ControllerBase, route
from ninja import Query
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated
from ninja.pagination import paginate
from utils.chen_pagination import MyPagination
from django.db import transaction
from typing import List
from utils.chen_response import ChenResponse
from apps.project.models import Design, Dut, Round, TestDemand, TestDemandContent, Case, CaseStep, Problem
from apps.project.schemas.problem import DeleteSchema, ProblemModelOutSchema, ProblemFilterSchema, \
    ProblemTreeReturnSchema, ProblemTreeInputSchema, ProblemCreateOutSchema, ProblemCreateInputSchema, \
    ProblemSingleInputSchema, ProblemUpdateInputSchema

@api_controller("/project", auth=JWTAuth(), permissions=[IsAuthenticated], tags=['问题单系列'])
class ProblemController(ControllerBase):
    @route.get("/getProblemList", response=List[ProblemModelOutSchema], exclude_none=True,
               url_name="problem-list")
    @transaction.atomic
    @paginate(MyPagination)
    def get_problem_list(self, data: ProblemFilterSchema = Query(...)):
        for attr, value in data.__dict__.items():
            if getattr(data, attr) is None:
                setattr(data, attr, '')
        case_key = "".join([data.round_id, '-', data.dut_id, '-', data.design_id, '-', data.test_id, '-', data.case_id])
        # 先查询出对应的case
        case_obj = Case.objects.filter(key=case_key).first()
        # 然后进行过滤
        qs = case_obj.caseField.filter(project__id=data.project_id,
                                       ident__icontains=data.ident,
                                       name__icontains=data.name,
                                       status__icontains=data.status,
                                       type__icontains=data.type,
                                       grade__icontains=data.grade,
                                       operation__icontains=data.operation,
                                       postPerson__icontains=data.postPerson,
                                       ).order_by("id")

        # 遍历通过代码不通过ORM查询闭环方式-巧妙使用numpy中array对象的in方法来判断
        closeMethod1 = self.context.request.GET.get("closeMethod[0]")
        closeMethod2 = self.context.request.GET.get("closeMethod[1]")
        query_final = []
        for query in qs:
            arr = np.array(query.closeMethod)
            if closeMethod1 is None and closeMethod2 is None:
                query_final.append(query)
                continue
            if closeMethod1 in arr:
                query_final.append(query)
                continue
            if closeMethod2 in arr:
                query_final.append(query)
                continue
        return query_final

    # 搜索全部问题单
    @route.get('/problem/searchAllProblem', response=List[ProblemModelOutSchema], exclude_none=True,
               url_name="problem-allList")
    @transaction.atomic
    @paginate(MyPagination)
    def get_all_problems(self, data: ProblemFilterSchema = Query(...)):
        for attr, value in data.__dict__.items():
            if getattr(data, attr) is None:
                setattr(data, attr, '')
        # 先查询当前项目
        qs = Problem.objects.filter(project__id=data.project_id,
                                    ident__icontains=data.ident,
                                    name__icontains=data.name,
                                    status__icontains=data.status,
                                    type__icontains=data.type,
                                    grade__icontains=data.grade,
                                    operation__icontains=data.operation,
                                    postPerson__icontains=data.postPerson,
                                    ).order_by("id")
        closeMethod1 = self.context.request.GET.get("closeMethod[0]")
        closeMethod2 = self.context.request.GET.get("closeMethod[1]")
        query_final = []
        for query in qs:
            arr = np.array(query.closeMethod)
            if closeMethod1 is None and closeMethod2 is None:
                query_final.append(query)
                continue
            if closeMethod1 in arr:
                query_final.append(query)
                continue
            if closeMethod2 in arr:
                query_final.append(query)
                continue
        # 遍历所有problem，查询是有否有关联case，如果有则设置hang为True，否则False
        hang = True
        for pro_obj in query_final:
            case_exists = pro_obj.case.exists()
            if not case_exists:
                hang = False
            setattr(pro_obj, "hang", hang)

        # 查询当前的case
        case_obj = Case.objects.filter(key=data.key).first()
        if case_obj:
            for pro_obj in query_final:
                # 查询关联的case
                related = False
                for re_case in pro_obj.case.all():
                    if case_obj.id == re_case.id:
                        related = True
                setattr(pro_obj, "related", related)
        return query_final

    # 添加问题单
    @route.post("/problem/save", response=ProblemCreateOutSchema, url_name="problem-create")
    @transaction.atomic
    def create_case_demand(self, payload: ProblemCreateInputSchema):
        asert_dict = payload.dict(exclude_none=True)
        # 构造case_key
        case_key = "".join(
            [payload.round_key, "-", payload.dut_key, '-', payload.design_key, '-', payload.test_key, '-',
             payload.case_key])
        # 查询出所属的case
        case_obj = Case.objects.filter(key=case_key).first()
        # 查询problem的总数
        problem_count = Problem.objects.filter(project_id=payload.project_id).count()
        # 查询当前各个前面节点的instance
        asert_dict.pop("round_key")
        asert_dict.pop("dut_key")
        asert_dict.pop("design_key")
        asert_dict.pop("test_key")
        asert_dict.pop("case_key")
        # 处理问题单标识PT_项目ident_数目依次增加
        asert_dict["ident"] = str(problem_count + 1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        qs = Problem.objects.create(**asert_dict)
        qs.case.add(case_obj)
        qs.save()
        return qs

    # 更新问题单
    @route.put("/problem/update/{id}", response=ProblemCreateOutSchema, url_name="problem-update")
    @transaction.atomic
    def update_problem(self, id: int, payload: ProblemCreateInputSchema):
        # 查到当前
        problem_qs = Problem.objects.get(id=id)
        for attr, value in payload.dict().items():
            setattr(problem_qs, attr, value)
        problem_qs.save()
        return ChenResponse(message="问题单更新成功")

    # 弹窗的-更新问题单
    @route.put("/problem/modalupdate/{id}", response=ProblemCreateOutSchema, url_name="problem-update")
    @transaction.atomic
    def update_modal_problem(self, id: int, payload: ProblemUpdateInputSchema):
        # 查到当前
        problem_qs = Problem.objects.get(id=id)
        for attr, value in payload.dict().items():
            setattr(problem_qs, attr, value)
        problem_qs.save()
        return ChenResponse(message="问题单更新成功")

    # 删除问题单
    @route.delete("/problem/delete", url_name="problem-delete")
    @transaction.atomic
    def delete_problem(self, data: DeleteSchema):
        # 1.查询出所有被删除id
        problems = Problem.objects.filter(id__in=data.ids)
        # 4.查询出当前项目id
        project_id = None
        # 2.循环该取出problem
        for problem in problems:
            project_id = problem.project_id
            # 3. 直接删除case关联，然后删除自己
            problem.case.clear()
            problem.delete()
        # 4.找到对应项目的所有problems进行排序
        if project_id is not None:
            index = 0
            for problem in Problem.objects.filter(project_id=project_id).order_by('id'):
                problem.ident = str(index + 1)
                problem.save()
                index += 1

        return ChenResponse(message="问题单删除成功！")

    # 单独显示问题单页面需要数据
    @route.get("/getSingleProblem", url_name="problem-single", response=ProblemCreateOutSchema)
    @transaction.atomic
    def search_single_problem(self, data: ProblemSingleInputSchema = Query(...)):
        key_string = "".join(
            [data.round_id, '-', data.dut_id, '-', data.design_id, '-', data.test_id, '-', data.case_id, '-',
             data.problem_id])
        qs = Problem.objects.get(project__id=data.project_id, key=key_string)
        return qs

    # 让测试用例关联/取消问题单
    @route.get('/problem/relateProblem', exclude_none=True, url_name="problem-allList")
    @transaction.atomic
    def relate_problem(self, case_key: str, problem_id: int, val: bool):  # val是将要变成的值
        # 先判断将要变成的值是否为True
        case_obj = Case.objects.filter(key=case_key).first()
        problem_obj = Problem.objects.filter(id=problem_id).first()
        flag = False  # 是否操作成功的标志
        if val:
            # 这分支是进行关联操作
            case_obj.caseField.add(problem_obj)
            flag = True
        else:
            # 这分支是取消关联操作 - 先要判断是否该问题单关联的测试用例只有一个了，如果只有一个则给前端返回错误
            if problem_obj:
                if problem_obj.case.count() < 2:
                    return ChenResponse(code=400, status=400, message='该问题必须关联至少一个用例',
                                        data={'isOK': False})
            case_obj.caseField.remove(problem_obj)
            flag = True
        return ChenResponse(code=200, status=200, message='关联或取消关联成功...', data={'isOK': flag})
