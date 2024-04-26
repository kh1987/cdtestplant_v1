from ninja_extra import NinjaExtraAPI
from django.http import HttpRequest, HttpResponse
from typing import Any

# 重写ninja返回 - 全局统一视图函数返回，如果None则如下返回
class ChenNinjaAPI(NinjaExtraAPI):
    def create_response(
            self, request: HttpRequest, data: Any, *, status: int = 200, code: int = 200, message: str = "请求成功",
            temporal_response: HttpResponse = None,
    ) -> HttpResponse:
        std_data = {
            "code": code,
            "data": data,
            "message": message,
            "success": True
        }
        # ninja_extra的APIException异常处理
        if 'detail' in std_data['data']:
            std_data['message'] = std_data['data']['detail']
        # ~~~~~~~~~~正常异常,status进行通用处理:TODO:后续规划~~~~~~~~~~
        if status == 403:
            std_data['message'] = '您没有权限这样做'
        elif status == 401:
            if std_data['data']['detail'] == '找不到指定凭据对应的有效用户':
                std_data['message'] = '账号或密码错误，如果是内网登录检查密码是否过期...'
                std_data['data']['code'] = 40001  # TODO:后续单独以枚举方式定义code
            else:
                std_data['message'] = '您的token已过期，请重新登录'
        elif status != 200 and std_data['message'] == '请求成功':
            std_data['message'] = '请求失败，请检查'

        content = self.renderer.render(request, std_data, response_status=status)
        content_type = "{}; charset={}".format(
            self.renderer.media_type, self.renderer.charset
        )
        return HttpResponse(content, status=status, content_type=content_type)
