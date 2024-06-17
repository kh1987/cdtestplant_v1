from typing import List
from ninja_extra import api_controller, ControllerBase, route
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated
from django.db.transaction import atomic
from apps.system.models import LoginLog, OperationLog
# 导入schemas
from apps.system.schemas.log import LogOutSchema, OperationLogOutSchema

@api_controller("/system/log", auth=JWTAuth(), permissions=[IsAuthenticated], tags=['日志相关'])
class LogController(ControllerBase):
    @route.get('/list', response=List[LogOutSchema])
    @atomic
    def get_login_log(self):
        """获取当前用户的登录日志"""
        user = self.context.request.user
        log_qs = LoginLog.objects.filter(creator=user)
        logs = log_qs[:5]
        return logs

    @route.get('/operations', response=List[OperationLogOutSchema])
    @atomic
    def get_operations(self):
        """获取当前用户操作日志"""
        user = self.context.request.user
        log_qs = OperationLog.objects.filter(creator=user)
        return log_qs[:5]
