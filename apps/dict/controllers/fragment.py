from typing import List
from ninja_extra import api_controller, ControllerBase, route
from ninja import Schema, Field, Query, ModelSchema
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated
from apps.dict.fragment.enums import DocNameEnum
# 小工具函数
from utils.smallTools.interfaceTools import conditionNoneToBlank
from ninja.pagination import paginate
from utils.chen_pagination import MyPagination
# ORM模型
from apps.dict.models import Fragment

# Schemas
## 查询fragment的输入
class FragementListSchema(Schema):
    belongDocName: DocNameEnum = None  # 所属产品文档名称
    name: str = None  # 片段名称
    isMain: bool = None  # 是否替换磁盘的片段
    project_id: int = Field(None, alias='projectId')

## 查询结果
class FragmentOutSchema(ModelSchema):
    class Meta:
        model = Fragment
        fields = ['id', 'name', 'belong_doc', 'project', 'field_seq', 'is_main']

# Controller
@api_controller("/system/userField", tags=['文档片段'], auth=JWTAuth(), permissions=[IsAuthenticated])
class UserFiledController(ControllerBase):
    @route.get("/getFragment", response=List[FragmentOutSchema], url_name='fragment-list')
    @paginate(MyPagination)
    def get_fragement(self, condition: Query[FragementListSchema]):
        conditionNoneToBlank(condition)
        return Fragment.objects.all()
