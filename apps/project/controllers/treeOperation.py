from ninja_extra import api_controller, ControllerBase, route
from ninja_jwt.authentication import JWTAuth
from ninja_extra.permissions import IsAuthenticated
from django.db import transaction

@api_controller("/treeOperation", auth=JWTAuth(), permissions=[IsAuthenticated], tags=['树的操作'])
class TreeController(ControllerBase):
    @route.get("/copy", url_name="tree-copy")
    @transaction.atomic
    def tree_copy(self):
        print('进入此处')
