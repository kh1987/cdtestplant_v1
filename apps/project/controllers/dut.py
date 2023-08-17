from ninja_extra import api_controller, ControllerBase, route
from ninja import Query
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated
from ninja.pagination import paginate
from utils.chen_pagination import MyPagination
from django.db import transaction
from typing import List
from utils.chen_response import ChenResponse
from utils.chen_crud import multi_delete
from apps.project.models import Dut, Round
from apps.project.schemas.dut import DutModelOutSchema, DutFilterSchema, DutTreeReturnSchema, DutTreeInputSchema, \
    DutCreateInputSchema, DutCreateOutSchema, DeleteSchema

@api_controller("/project", auth=JWTAuth(), permissions=[IsAuthenticated], tags=['被测件数据'])
class DutController(ControllerBase):
    @route.get("/getDutList", response=List[DutModelOutSchema], exclude_none=True, url_name="dut-list")
    @transaction.atomic
    @paginate(MyPagination)
    def get_dut_list(self, filters: DutFilterSchema = Query(...)):
        for attr, value in filters.__dict__.items():
            if getattr(filters, attr) is None:
                setattr(filters, attr, '')
        qs = Dut.objects.filter(project__id=filters.project_id, round__key=filters.round_id,
                                ident__icontains=filters.ident,
                                name__icontains=filters.name,
                                type__contains=filters.type).order_by("-create_datetime")
        return qs

    # 处理树状数据
    @route.get("/getDutInfo", response=List[DutTreeReturnSchema], url_name="dut-info")
    def get_round_tree(self, payload: DutTreeInputSchema = Query(...)):
        qs = Dut.objects.filter(project__id=payload.project_id, round__key=payload.key)
        return qs

    # 添加被测件
    @route.post("/dut/save", response=DutCreateOutSchema, url_name="dut-create")
    @transaction.atomic
    def create_dut(self, payload: DutCreateInputSchema):
        asert_dict = payload.dict(exclude_none=True)
        # 判重标识
        if Dut.objects.filter(project__id=payload.project_id, round__key=payload.round_key,
                              ident=payload.ident).exists():
            return ChenResponse(code=400, status=400, message='被测件的标识重复，请检查')
        # 查询当前key应该为多少
        dut_count = Dut.objects.filter(project__id=payload.project_id, round__key=payload.round_key).count()
        key_string = ''.join([payload.round_key, "-", str(dut_count)])
        # 查询当前的round_id
        round_instance = Round.objects.get(project__id=payload.project_id, key=payload.round_key)
        asert_dict.update({'key': key_string, 'round': round_instance, 'title': payload.name})
        asert_dict.pop("round_key")
        qs = Dut.objects.create(**asert_dict)
        return qs

    # 更新被测件
    @route.put("/dut/update/{id}", url_name="dut-update", response=DutCreateOutSchema)
    @transaction.atomic
    def update_dut(self, id: int, payload: DutCreateInputSchema):
        dut_search = Dut.objects.filter(project__id=payload.project_id, ident=payload.ident)
        # 判断是否和同项目同轮次的标识重复
        if len(dut_search) > 1:
            return ChenResponse(code=400, status=400, message='被测件的标识重复，请检查')
        # 查到当前
        if payload.type == 'SO':
            dut_qs = Dut.objects.get(id=id)
            for attr, value in payload.dict().items():
                if attr == 'project_id' or attr == 'round_key':
                    continue
                if attr == 'name':
                    setattr(dut_qs, "title", value)
                setattr(dut_qs, attr, value)
            dut_qs.save()
            return dut_qs
        else:
            dut_qs = Dut.objects.get(id=id)
            for attr, value in payload.dict().items():
                if attr == 'project_id' or attr == 'round_key':
                    continue
                if attr == 'black_line' or attr == 'comment_line' or attr == 'pure_code_line' or attr == 'total_code_line' or attr == 'total_comment_line' or attr == 'total_line' or attr == 'mix_line':
                    setattr(dut_qs, attr, "")
                    continue
                if attr == 'name':
                    setattr(dut_qs, "title", value)
                setattr(dut_qs, attr, value)
            dut_qs.save()
            return dut_qs

    # 删除被测件
    @route.delete("/dut/delete", url_name="dut-delete")
    @transaction.atomic
    def delete_dut(self, data: DeleteSchema):
        dut_single = Dut.objects.filter(id=data.ids[0])[0]
        round_id = dut_single.round.id
        round_key = dut_single.round.key
        multi_delete(data.ids, Dut)
        index = 0
        dut_all_qs = Dut.objects.filter(round__id=round_id)
        for single_qs in dut_all_qs:
            dut_key = "".join([round_key, '-', str(index)])
            single_qs.key = dut_key
            index = index + 1
            single_qs.save()
        return ChenResponse(message="被测件删除成功！")
