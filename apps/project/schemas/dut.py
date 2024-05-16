from apps.project.models import Dut
from ninja import Field, Schema, ModelSchema
from typing import List, Union, Optional
from datetime import date

class DutModelOutSchema(ModelSchema):
    class Config:
        model = Dut
        model_exclude = ['project', 'round', 'remark', 'sort']

class DutFilterSchema(Schema):
    project_id: int = Field(None, alias='projectId')
    round_id: int = Field(None, alias='round')
    ident: str = Field(None, alias='ident')
    type: str = Field(None, alias='type')
    name: str = Field(None, alias='name')
    # 新增版本、单位
    version: str = Field(None, alias="version")
    release_union: str = Field(None, alias="release_union")

# 树状目录schema
class DutTreeInputSchema(Schema):
    # 注意这里有alias
    project_id: int = Field(None, alias='projectId')
    key: str = Field(None, alias='key')
    level: str = Field(None, alias='level')

class DutTreeReturnSchema(Schema):
    title: str = Field(..., alias='title')
    key: str = Field(..., alias='key')
    level: str = Field(..., alias='level')

# 新增接口schema
class DutCreateInputSchema(Schema):
    project_id: int = Field(..., alias="projectId")
    round_key: str = Field(..., alias="round")
    ident: str = Field(None, alias="ident")
    name: str = Field(None, alias="name")
    type: str = Field(None, alias="type")
    black_line: Union[str, int] = Field(None, alias="black_line")
    code_line: Union[str, int] = Field(None, alias="code_line")
    mix_line: Union[str, int] = Field(None, alias="mix_line")
    comment_line: Union[str, int] = Field(None, alias="comment_line")
    # 新增版本、单位、发布日期
    version: str = Field(None, alias="version")
    release_union: str = Field(None, alias="release_union")
    release_date: str = Field(None, alias="release_date")
    # 新增用户标识
    ref: str = Field(None, alias='ref')

# 不能去掉，这个决定前端动态刷新树状目录
class DutCreateOutSchema(ModelSchema):
    level: Union[str, int]
    black_line: Optional[Union[str, int]] = None
    code_line: Optional[Union[str, int]] = None
    mix_line: Optional[Union[str, int]] = None
    comment_line: Optional[Union[str, int]] = None

    class Config:
        model = Dut
        model_exclude = ['remark', 'sort', 'project', 'round']

# 删除schema
class DeleteSchema(Schema):
    ids: List[int]

# 第一轮如果没有源代码被测的新增so的schema
class DutCreateR1SoDutSchema(Schema):
    project_id: int
    version: str
    ref: str = Field(..., alias='userRef')
    release_union: str = Field(..., alias='unit')
    release_date: date = Field(..., alias='date')
    black_line: Union[str, int] = None
    code_line: Union[str, int] = None
    mix_line: Union[str, int] = None
    comment_line: Union[str, int] = None
    # 5月17日新增轮次的key
    round_key: str
