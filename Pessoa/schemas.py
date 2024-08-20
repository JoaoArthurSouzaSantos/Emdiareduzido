from pydantic import BaseModel
from datetime import date

class PessoaBase(BaseModel):
    nome: str
    cpf: str # CPF como inteiro
    email: str

class PessoaCreate(PessoaBase):
    pass

class PessoaOut(PessoaBase):
    class Config:
        orm_mode = True
