from pydantic import BaseModel
from datetime import date
from typing import Optional,List


class PacienteCreate(BaseModel):
    data_nascimento: date
    numeroSUS: str
    id_paciente: str  
    sexo : str
    info: str

    class Config:
        orm_mode = True

class PacienteOut(BaseModel):
    numeroSUS: str
    id_paciente: str  
    sexo : str
    info: str
    data_nascimento: date
    class Config:
        orm_mode = True

class ConsultaOut(BaseModel):
    id: int
    id_paciente: str
    id_funcionario: str
    data: date
    hbg: Optional[float]
    tomaMedHipertensao: Optional[str]
    praticaAtivFisica: Optional[str]
    imc: Optional[float]
    peso: Optional[float]
    historicoAcucarElevado: Optional[str]
    altura: Optional[float]
    cintura: Optional[float]
    resultadoFindRisc: Optional[str]
    frequenciaIngestaoVegetaisFrutas: Optional[str]
    historicoFamiliar: Optional[str]
    dataRetorno: Optional[date]
    medico: Optional[str]

    class Config:
        orm_mode = True

class PacienteOut(BaseModel):
    numeroSUS: str
    id_paciente: str
    data_nascimento: date
    sexo: str
    info: str

    class Config:
        orm_mode = True

class PacienteWithConsultasOut(PacienteOut):
    consultas: List[ConsultaOut]


# Define o schema para a saída de Paciente com informações de Pessoa
class PacienteWithPessoaOut(BaseModel):
    # Campos de Paciente
    numeroSUS: str
    id_paciente: str
    data_nascimento: date
    sexo: str
    info: str

    # Campos de Pessoa
    cpf: str
    nome: str
    email: str

    class Config:
        orm_mode = True