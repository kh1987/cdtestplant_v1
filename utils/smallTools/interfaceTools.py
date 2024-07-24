from ninja import Schema

def conditionNoneToBlank(condition: Schema):
    """将BaseModel/Schema对象中None变为空字符串"""
    for attr, value in condition.__dict__.items():
        if getattr(condition, attr) is None:
            setattr(condition, attr, '')
