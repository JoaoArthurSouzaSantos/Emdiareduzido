import re
from pydantic import BaseModel, validator


class FuncionarioSchema(BaseModel):
    username: str
    password: str
    id: str

    @validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[0-9]|@)+$', value):
            raise ValueError('Username format invalid')
        return value

class FuncionarioLogin(BaseModel):
    username: str
    password: str

    @validator('username')
    def validate_username(cls, value):
        if not re.match('^([a-z]|[0-9]|@)+$', value):
            raise ValueError('Username format invalid')
        return value

