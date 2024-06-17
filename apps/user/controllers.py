from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from ninja_extra import api_controller, ControllerBase, status, route
from ninja.pagination import paginate
from utils.chen_pagination import MyPagination
from ninja_extra.permissions import IsAuthenticated, IsAdminUser
from ninja import Query
from django.db import transaction
from ninja_jwt.tokens import RefreshToken
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.controller import TokenObtainPairController
from ninja_jwt import schema
from typing import List
from utils.chen_response import ChenResponse
from apps.user.schema import UserInfoOutSchema, CreateUserSchema, CreateUserOutSchema, UserRetrieveInputSchema, \
    UserRetrieveOutSchema, UpdateDeleteUserSchema, UpdateDeleteUserOutSchema, DeleteUserSchema, LogOutSchema, \
    LogInputSchema, LogDeleteInSchema
from apps.user.models import OperationLog

# 工具函数
from utils.chen_crud import update, multi_delete
from apps.user.tools.ldap_tools import load_ldap_users
# 导入登录日志函数
from utils.log_util.request_util import save_login_log

Users = get_user_model()

# 定义用户登录接口，包含token刷新和生成
@api_controller("/system", tags=['用户token控制和登录接口'])
class UserTokenController(TokenObtainPairController):
    auto_import = True

    @route.post("/login", url_name='login')
    def obtain_token(self, user_token: schema.TokenObtainPairSerializer):
        """新版本有特性，后期修改"""
        # 注意TokenObtainPairSerializer是老版本，所以兼容，本质是TokenObtainPairInputSchema
        user = user_token._user
        if user:
            save_login_log(request=self.context.request, user=user)  # 保存登录日志
        refresh = RefreshToken.for_user(user)
        token = refresh.access_token  # type:ignore
        return ChenResponse(code=200,
                            data={'token': str(token), 'refresh': str(refresh),
                                  'token_exp_data': datetime.utcfromtimestamp(token["exp"])})

    @route.get("/getInfo", response=UserInfoOutSchema, url_name="get_info", auth=JWTAuth())
    def get_user_info(self):
        # 直接按照Schema返回
        return self.context.request.auth

    @route.post("/logout", url_name="logout", auth=JWTAuth())
    def logout(self):
        return ChenResponse(code=200, message='退出登录成功')

# 定义system/user用户管理接口
@api_controller("/system/user", tags=['用户管理'], auth=JWTAuth())
class UserManageController(ControllerBase):
    # 用户创建接口
    @route.post("/save", response={201: CreateUserOutSchema}, url_name="user_create", auth=None)
    def create_user(self, user_schema: CreateUserSchema):
        user = user_schema.create()
        return user

    # 给前端传所有用户当做字典
    @route.get('/list', response=List[UserRetrieveOutSchema], url_name="user_list", auth=None)
    @transaction.atomic
    def list_user(self):
        qs = Users.objects.all()
        return qs

    # 用户检索接口
    @route.get("/index", response=List[UserRetrieveOutSchema])
    @paginate(MyPagination)
    def index_user(self, filters: UserRetrieveInputSchema = Query(...)):
        # 重要，处理前端不传值为None的情况
        for attr, value in filters.__dict__.items():
            if getattr(filters, attr) is None:
                setattr(filters, attr, '')
        start_time = self.context.request.GET.get('create_datetime[0]')
        if start_time is None:
            start_time = "2000-01-01"
        end_time = self.context.request.GET.get('create_datetime[1]')
        if end_time is None:
            end_time = '8000-01-01'
        date_list = [start_time, end_time]
        qs = Users.objects.filter(name__icontains=filters.name, username__icontains=filters.username,
                                  phone__icontains=filters.phone, status__contains=filters.status,
                                  create_datetime__range=date_list).order_by('-create_datetime')
        return qs

    @route.put("/update/{user_id}", response=UpdateDeleteUserOutSchema, permissions=[IsAuthenticated, IsAdminUser],
               url_name="user-update")
    def update_user(self, user_id: int, payload: UpdateDeleteUserSchema):
        if payload.username == "superAdmin":
            return ChenResponse(code=400, status=400, message="无法编辑，唯一管理员账号")
        update_user = update(self.context.request, user_id, payload, Users)
        return {"message": "用户更新成功"}

    @route.delete("/delete", permissions=[IsAuthenticated, IsAdminUser], url_name="user-delete")
    def delete_user(self, data: DeleteUserSchema):
        ids = data.ids
        # 去掉删除创始人
        for item in ids:
            if item == 1:
                ids.pop(item)
        multi_delete(ids, Users)
        return ChenResponse(code=200, status=200, message="删除成功")

    @route.get("/ldap", url_name='user-ldap')
    def load_ldap(self):
        try:
            load_ldap_users()
            return ChenResponse(status=200, code=200, message='加载LDAP用户成功，并同步数据库')
        except Exception as exc:
            print(exc)
            return ChenResponse(status=500, code=500, message='加载LDAP用户错误')

# 操作日志接口
@api_controller("/system/log", tags=['日志记录'], auth=JWTAuth())
class LogController(ControllerBase):
    @route.get("/operation_list", url_name="log_list", response=List[LogOutSchema], auth=None)
    @paginate(MyPagination)
    def log_list(self, data: Query[LogInputSchema]):
        for attr, value in data.model_dump().items():
            if getattr(data, attr) is None:
                setattr(data, attr, '')
        logs = OperationLog.objects.values('id', 'user__username', 'operate_obj', 'create_datetime',
                                           'operate_des').order_by(
            '-create_datetime')
        # 根据条件搜索
        logs = logs.filter(user__username__icontains=data.user, create_datetime__range=data.create_datetime)
        return logs

    @route.get('/operation_delete', url_name='log_delete', permissions=[IsAuthenticated, IsAdminUser], auth=JWTAuth())
    def log_delete(self, data: LogDeleteInSchema = Query(...)):
        time = datetime.now() - timedelta(days=data.day)
        log_qs = OperationLog.objects.filter(create_datetime__lt=time)
        log_qs.delete()
        if data.day > 0:
            return ChenResponse(message=f'删除{data.day}天前数据成功')
        else:
            return ChenResponse(message='全部日志删除成功')
