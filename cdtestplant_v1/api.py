from utils.chen_ninja import ChenNinjaAPI
from utils.chen_response import ChenResponse
from ninja.errors import ValidationError
from ninja import Redoc
from ninja_extra import exceptions
# 导入解析器，渲染器
from cdtestplant_v1.parser import MyParser
from cdtestplant_v1.renderer import MyRenderer

api = ChenNinjaAPI(
    title="成都测试平台API",
    description="成都测试平台的接口一系列接口函数",
    urls_namespace="cdtestplant_v1",
    parser=MyParser(),
    renderer=MyRenderer()
)

""" 暂未用到该代码
# 处理jwt错误的APIException问题
@api.exception_handler(exceptions.APIException)
def api_exception_handler(request, exc):
    headers = {}
    if isinstance(exc.detail, (list, dict)):
        data = exc.detail
    else:
        data = {"detail": exc.detail}

    response = api.create_response(request, data, status=exc.status_code)
    for k, v in headers.items():
        response.setdefault(k, v)
    return response
"""

# ninja_extra特性:自动寻找apps里面的Controller
api.auto_discover_controllers()
