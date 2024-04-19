from pydantic import BaseModel

class Model(BaseModel):
    x: str

print(Model(x=123))
