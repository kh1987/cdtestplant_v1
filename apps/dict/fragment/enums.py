from enum import Enum, unique

# 产品文档名称
@unique
class DocNameEnum(Enum):
    dg = '大纲'
    sm = '说明'
    jl = '记录'
    hsm = '回归说明'
    hjl = '回归记录'
    bg = '报告'
    wtd = '问题单'
