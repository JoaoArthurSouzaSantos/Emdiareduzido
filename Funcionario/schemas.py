from pydantic import BaseModel

class FuncionarioCreate(BaseModel):
    id: str
    username: str
    password: str

    class Config:
        orm_mode = True

class FuncionarioOut(BaseModel):
    id: str
    username: str

    class Config:
        orm_mode = True
