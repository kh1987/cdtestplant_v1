from datetime import date
from ninja_extra import api_controller, ControllerBase, route
from ninja import Query
from apps.dict.models import Dict, DictItem
from apps.project.models import Contact, Abbreviation, Project
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated, IsAdminUser
from ninja.pagination import paginate
from utils.chen_pagination import MyPagination
from django.db import transaction
from django.contrib.auth import get_user_model
from typing import List
from utils.chen_crud import multi_delete
from utils.chen_response import ChenResponse
from apps.dict.schema import DictItemOut, DictOut, DictIndexInput, ChangeStautsSchemaInput, DictItemInput, DictItemOut, \
    DictItemChangeSrotInput, DictItemCreateInputSchema, DictItemUpdateInputSchema, DeleteSchema, ContactListInputSchema, \
    ContactOut, AbbreviationOut, AbbreviationListInputSchema

Users = get_user_model()

@api_controller("/system", tags=['字典相关'], auth=JWTAuth(), permissions=[IsAuthenticated])
class DictController(ControllerBase):
    @route.get("/dataDict/list", response=List[DictItemOut], url_name="dict-list")
    def get_dict(self, code: str):
        """传入code类型：例如testType，返回字典Item信息"""
        dict_qs = Dict.objects.get(code=code)
        items = dict_qs.dictItem.filter(status='1')
        return items

    @route.get("/dataDict/index", response=List[DictOut], url_name="dict-index")
    @transaction.atomic
    @paginate(MyPagination)
    def get_dict_index(self, payload: DictIndexInput = Query(...)):
        for attr, value in payload.__dict__.items():
            if getattr(payload, attr) is None:
                setattr(payload, attr, '')
        # 处理时间
        if payload.update_datetime_start == '':
            payload.update_datetime_start = "2000-01-01"
        if payload.update_datetime_end == '':
            payload.update_datetime_end = '5000-01-01'
        date_list = [payload.update_datetime_start, payload.update_datetime_end]
        qs = Dict.objects.filter(name__icontains=payload.name, remark__icontains=payload.remark,
                                 code__icontains=payload.code, status__icontains=payload.status,
                                 update_datetime__range=date_list)
        return qs

    @route.put("/dataDict/changeStatus", url_name="dict-changeStatus", permissions=[IsAdminUser])
    @transaction.atomic
    def change_dict_status(self, data: ChangeStautsSchemaInput):
        qs = Dict.objects.get(id=data.id)
        qs.status = data.status
        qs.save()
        return ChenResponse(code=200, status=200, message="修改状态成功")

    @route.put("/dataDict/changeItemStatus", url_name="dict-changeItemStatus", permissions=[IsAdminUser])
    @transaction.atomic
    def change_dict_item_status(self, data: ChangeStautsSchemaInput):
        qs = DictItem.objects.get(id=data.id)
        qs.status = data.status
        qs.save()
        return ChenResponse(code=200, status=200, message="修改状态成功")

    # 有dict的id查询其中的dictItem数据
    @route.get("/dataDict/dictItemAll", response=List[DictItemOut], url_name='dictitem-list')
    @transaction.atomic
    @paginate(MyPagination)
    def get_dictItem_list(self, payload: DictItemInput = Query(...)):
        for attr, value in payload.__dict__.items():
            if getattr(payload, attr) is None:
                setattr(payload, attr, '')
        # 处理时间
        if payload.update_datetime_start == '':
            payload.update_datetime_start = "2000-01-01"
        if payload.update_datetime_end == '':
            payload.update_datetime_end = '5000-01-01'
        date_list = [payload.update_datetime_start, payload.update_datetime_end]
        # 先对dict_id进行查询
        dict_qs = Dict.objects.get(id=payload.dict_id)
        # 反向连接
        qs = dict_qs.dictItem.filter(update_datetime__range=date_list, status__icontains=payload.status,
                                     key__icontains=payload.key, title__icontains=payload.title,
                                     show_title__icontains=payload.show_title).order_by('sort')
        return qs

    # 更改dictItem的sort字段接口
    @route.put("/dataDict/numberOperation", url_name="dictitem-changesort")
    @transaction.atomic
    def change_item_sort(self, data: DictItemChangeSrotInput):
        qs = DictItem.objects.get(id=data.id)
        qs.sort = data.numberValue
        qs.save()
        return ChenResponse(code=200, status=200, message='排序序号更新成功')

    # 新增dictItem
    @route.post("/dataDict/saveitem", response=DictItemOut, url_name="dictitem-save")
    @transaction.atomic
    def save(self, payload: DictItemCreateInputSchema):
        # 先根据dict_id查询出dict
        dict_qs = Dict.objects.get(id=payload.dict_id)
        qs1 = dict_qs.dictItem.filter(title=payload.title)
        if len(qs1) > 0:
            return ChenResponse(code=400, status=400, message='字典标签重复，请检查')
        # 计算key值应该为多少
        key_number = str(len(dict_qs.dictItem.all()) + 1)
        asert_dict = payload.dict(exclude_none=True)
        asert_dict.pop('dict_id')
        asert_dict.update({'dict': dict_qs, 'key': key_number})
        qs = DictItem.objects.create(**asert_dict)
        return qs

    # 更新dictitem数据
    @route.put("/dataDict/update/{id}", response=DictItemOut, url_name='dictitem-update')
    @transaction.atomic
    def update(self, id: int, payload: DictItemUpdateInputSchema):
        dictitem_qs = DictItem.objects.get(id=id)
        for attr, value in payload.dict().items():
            setattr(dictitem_qs, attr, value)
        dictitem_qs.save()
        return dictitem_qs

    # 删除dictItem数据
    @route.delete("/dictType/realDeleteItem", url_name="dictitem-delete", permissions=[IsAdminUser])
    @transaction.atomic
    def delete_dictitem(self, data: DeleteSchema):
        # 根据其中一个id查询出dict的id
        dictItem_single = DictItem.objects.filter(id=data.ids[0])[0]
        dict_id = dictItem_single.dict.id
        multi_delete(data.ids, DictItem)
        index = 1
        qs = Dict.objects.get(id=dict_id).dictItem.all()
        for qs_item in qs:
            qs_item.key = str(index)
            index = index + 1
            qs_item.save()
        return ChenResponse(message="字典条目删除成功！")

# 公司信息处理接口
@api_controller("/system", tags=['公司信息相关'], auth=JWTAuth(), permissions=[IsAuthenticated])
class ContactController(ControllerBase):
    @route.get("/contact/getlist", response=List[ContactOut], url_name="contact-search")
    @transaction.atomic
    @paginate(MyPagination)
    def get_contact_list(self, payload: ContactListInputSchema = Query(...)):
        for attr, value in payload.__dict__.items():
            if getattr(payload, attr) is None:
                setattr(payload, attr, '')
        if payload.key == '':
            qs = Contact.objects.filter(name__icontains=payload.name, entrust_person__icontains=payload.entrust_person,
                                        addr__icontains=payload.addr)
        else:
            qs = Contact.objects.filter(name__icontains=payload.name, entrust_person__icontains=payload.entrust_person,
                                        key=int(payload.key), addr__icontains=payload.addr)
        return qs

    # 单独获取
    @route.get("/contact/index", response=List[ContactOut], url_name="contact-all")
    @transaction.atomic
    def get_contact_index(self):
        qs = Contact.objects.all()
        return qs

    @route.post("/contact/save", response=ContactOut, url_name='contact-create')
    @transaction.atomic
    def create_contact(self, data: ContactListInputSchema):
        for attr, value in data.__dict__.items():
            if getattr(data, attr) is None:
                setattr(data, attr, '')
        # 判重key
        assert_dict = data.dict()
        key_qs = Contact.objects.filter(key=str(data.key))
        if len(key_qs) > 0:
            return ChenResponse(code=400, status=400, message="公司或单位的编号重复，请修改")
        # 全称判重
        name_qs = Contact.objects.filter(name=data.name)
        if len(name_qs) > 0:
            return ChenResponse(code=400, status=400, message="全称重复，请修改")

        qs = Contact.objects.create(**assert_dict)
        return qs

    @route.put("/contact/update/{id}", response=ContactOut, url_name='contact-update')
    @transaction.atomic
    def update_contact(self, id: int, data: ContactListInputSchema):
        for attr, value in data.__dict__.items():
            if getattr(data, attr) is None:
                setattr(data, attr, '')
        qs = Contact.objects.filter(id=id).first()
        if qs:
            if qs.key != data.key:
                key_qs = Contact.objects.filter(key=str(data.key))
                if len(key_qs) > 0:
                    return ChenResponse(code=400, status=400, message="公司或单位的编号重复，请修改")
            if qs.name != data.name:
                name_qs = Contact.objects.filter(name=data.name)
                print(name_qs)
                if len(name_qs) > 0:
                    return ChenResponse(code=400, status=400, message="全称重复，请修改")
            # 更新联系人数据
            for attr, value in data.__dict__.items():
                setattr(qs, attr, value)
            qs.save()
            return qs

    @route.delete('/contact/delete', url_name='contact-delete')
    @transaction.atomic
    def delete_contact(self, data: DeleteSchema):
        multi_delete(data.ids, Contact)
        return ChenResponse(message='单位或公司删除成功')

# 这是其他common内容接口
@api_controller("/system", tags=['通用接口'])
class CommonController(ControllerBase):
    @route.get("/getNoticeList")
    def get_notice(self, pageSize, orderBy, orderType):
        item_list = []
        item1 = {"title": "测试管理平台V0.0.2测试发布", "created_at": "2023-09-23",
                 "content": "测试管理平台V0.0.2发布，正在进行内部测试.."}
        item_list.append(item1)
        item2 = {"title": "测试管理平台更新公共", "created_at": "2024-06-17", "content": "<p>1.修改大纲和报告模版<p><p>2.修复多个bug<p>"}
        item_list.append(item2)
        return item_list

    @route.get('/workplace/statistics')
    @transaction.atomic
    def get_statistics(self):
        # 查询用户数量，进行的项目，项目总数，已完成项目数
        user_count = Users.objects.count()
        project_qs = Project.objects.all()
        project_count = project_qs.count()
        project_done_count = project_qs.filter(step='3').count()
        project_processing_count = project_qs.filter(step='1').count()
        return ChenResponse(data={'pcount': project_count, 'ucount': user_count,
                                  'pdcount': project_done_count, 'ppcount': project_processing_count})

    @route.get('/statistics/chart')
    @transaction.atomic
    def get_chart(self):
        """该接口返回当前年份下，每月的项目统计，返回横坐标12个月的字符串以及12个月数据"""
        current_year = date.today().year
        month_list = []
        # 构造数组，里面是字典
        for i in range(12):
            month_dict = {'month': i + 1, 'count': 0}
            month_list.append(month_dict)
        project_qs = Project.objects.all()
        for project in project_qs:
            for m in month_list:
                if m['month'] == project.beginTime.month and project.beginTime.year == current_year:
                    m['count'] += 1
        return ChenResponse(status=200, code=200, data=month_list)

@api_controller("/system", tags=['缩略语接口'], auth=JWTAuth(), permissions=[IsAuthenticated])
class AbbreviationController(ControllerBase):
    @route.get("/abbreviation/getlist", response=List[AbbreviationOut], url_name="abbreviation-search")
    @transaction.atomic
    @paginate(MyPagination)
    def get_abbreviation_list(self, payload: AbbreviationListInputSchema = Query(...)):
        for attr, value in payload.__dict__.items():
            if getattr(payload, attr) is None:
                setattr(payload, attr, '')
        qs = Abbreviation.objects.filter(title__icontains=payload.title, des__icontains=payload.des)
        return qs

    # 单独获取
    @route.get("/abbreviation/index", response=List[AbbreviationOut], url_name="abbreviation-all")
    @transaction.atomic
    def get_contact_index(self):
        qs = Abbreviation.objects.all()
        return qs

    @route.post("/abbreviation/save", response=AbbreviationOut, url_name='abbreviation-create')
    @transaction.atomic
    def create_abbreviation(self, data: AbbreviationListInputSchema):
        for attr, value in data.__dict__.items():
            if getattr(data, attr) is None:
                setattr(data, attr, '')
        # 判重key
        assert_dict = data.dict()
        key_qs = Abbreviation.objects.filter(title=data.title)
        if len(key_qs) > 0:
            return ChenResponse(code=400, status=400, message="缩略语重复，请修改...")
        # 正常添加
        qs = Abbreviation.objects.create(**assert_dict)
        return qs

    @route.put("/abbreviation/update/{id}", response=AbbreviationOut, url_name='abbreviation-update')
    @transaction.atomic
    def update_contact(self, id: int, data: AbbreviationListInputSchema):
        for attr, value in data.__dict__.items():
            if getattr(data, attr) is None:
                setattr(data, attr, '')
        key_qs = Abbreviation.objects.filter(title=data.title)
        if len(key_qs) > 1:
            return ChenResponse(code=400, status=400, message="缩略语重复，请修改...")
        # 查询id
        qs = Abbreviation.objects.get(id=id)
        for attr, value in data.__dict__.items():
            setattr(qs, attr, value)
        qs.save()
        return qs

    @route.delete('/abbreviation/delete', url_name='abbreviation-delete')
    @transaction.atomic
    def delete_contact(self, data: DeleteSchema):
        multi_delete(data.ids, Abbreviation)
        return ChenResponse(message='单位或公司删除成功')
