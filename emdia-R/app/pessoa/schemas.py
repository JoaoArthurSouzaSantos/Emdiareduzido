from pydantic import BaseModel
from datetime import date

class PessoaBase(BaseModel):
    nome: str
    cpf: str # CPF como inteiro
    email: str

class PessoaCreate(PessoaBase):
    nome: str
    cpf: str # CPF como inteiro
    email: str

class PessoaOut(PessoaBase):
    class Config:
        orm_mode = True
