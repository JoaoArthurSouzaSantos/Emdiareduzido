from pydantic import BaseModel
from datetime import date
from typing import Optional


class PacienteCreate(BaseModel):
    data_nascimento:  date
    numeroSUS: int
    id_paciente: str  
    sexo : str
    info: str

    class Config:
        orm_mode = True

class PacienteOut(BaseModel):
    numeroSUS: int
    id_paciente: str  
    sexo : str
    info: str

    class Config:
        orm_mode = True

class PessoaOut(BaseModel):
    cpf: str
    nome: str
    email: str

    class Config:
        orm_mode = True

class PacienteWithPessoaOut(BaseModel):
    numeroSUS: int
    id_paciente: str
    data_nascimento: Optional[date]  # ou Date
    sexo: Optional[str]
    info: Optional[str]
    pessoa: PessoaOut

    class Config:
        orm_mode = True

