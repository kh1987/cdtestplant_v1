from apps.project.models import Project
from ninja import Schema, ModelSchema
from typing import List, Optional

class ProjectRetrieveSchema(ModelSchema):
    class Config:
        model = Project
        model_exclude = ['update_datetime', 'create_datetime', 'remark']

class ProjectFilterSchema(Schema):
    ident: Optional[str] = None
    name: Optional[str] = None
    duty_person: Optional[str] = None
    security_level: Optional[str] = None
    report_type: Optional[str] = None
    step: Optional[str] = None
    # 新增软件类型：新研/改造
    soft_type: str = None

class ProjectCreateInput(ModelSchema):
    class Config:
        model = Project
        model_exclude = ['remark', 'update_datetime', 'create_datetime', 'sort', 'id']

class DeleteSchema(Schema):
    ids: List[int]
