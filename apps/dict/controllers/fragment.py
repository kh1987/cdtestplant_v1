from typing import List, Union
from ninja_extra import api_controller, ControllerBase, route
from ninja import Schema, Field, Query, ModelSchema
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated
# 小工具函数
from utils.smallTools.interfaceTools import model_retrieve
from ninja.pagination import paginate
from utils.chen_pagination import MyPagination
from utils.chen_crud import updateWithoutRequestParam, multi_delete
# ORM模型
from apps.dict.models import Fragment
# fragment操作类代入
from apps.dict.fragment.fragmentOperation import FragmentOperation

# Schemas
## 查询fragment的输入
class FragementListSchema(Schema):
    belong_doc: Union[int, str] = None  # 所属产品文档名称
    name: str = None  # 片段名称
    is_main: bool = None  # 是否替换磁盘的片段
    project_id: int = Field(None, alias='projectId')

## 查询结果
class FragmentOutSchema(ModelSchema):
    class Meta:
        model = Fragment
        fields = ['id', 'name', 'belong_doc', 'project', 'is_main', 'content']

## 更新文档片段
class FragmentUpdateSchema(Schema):
    name: str = None
    is_main: bool = None
    belong_doc: Union[int, str] = Field(None, alias='belong_doc')
    project_id: int = Field(None, alias='projectId')
    content: str = Field(None, alias='content')

# 删除schema
class FragmentDeleteSchema(Schema):
    ids: List[int]

# 全局静态变量
PIC_URL_PREFIX = "/uploads/"

# Controller
@api_controller("/system/userField", tags=['文档片段'], auth=JWTAuth(), permissions=[IsAuthenticated])
class UserFiledController(ControllerBase):
    @route.get("/getFragment", response=List[FragmentOutSchema], url_name='fragment-list')
    @paginate(MyPagination)
    def get_fragement(self, condition: Query[FragementListSchema]):
        fragment_qs = Fragment.objects.filter(project_id=condition.project_id)
        res_qs = model_retrieve(condition, fragment_qs, ['project_id', 'is_main'])
        return res_qs

    @route.delete("/delete", url_name="fragment-delete")
    def delete_fragment(self, data: FragmentDeleteSchema):
        try:
            multi_delete(data.ids, Fragment)
        except Exception:
            raise HttpError(500, "删除失败")

    @route.put("/update/{int:id}", url_name='fragment-update')
    def update_fragment(self, id: int, data: FragmentUpdateSchema):
        update_obj = updateWithoutRequestParam(id, data, Fragment)
        if update_obj:
            return '更新成功'
        raise HttpError(500, "设置替换磁盘文件渲染失败")
