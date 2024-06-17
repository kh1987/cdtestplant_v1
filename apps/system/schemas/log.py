from ninja import ModelSchema
from apps.system.models import LoginLog, OperationLog

# 1.登录日志输出schema
class LogOutSchema(ModelSchema):
    class Meta:
        model = LoginLog
        fields = ['id', 'username', 'agent', 'ip', 'browser', 'os', 'create_datetime']

# 2.操作日志输出shcema
class OperationLogOutSchema(ModelSchema):
    class Meta:
        model = OperationLog
        exclude = ['remark', 'modifier', 'request_modular', 'request_msg', 'sort', 'creator']
