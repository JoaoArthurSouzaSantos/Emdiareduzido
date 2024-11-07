from pydantic import BaseModel
from datetime import date
from typing import Optional
from typing import List

class PacienteCreate(BaseModel):
    dataNascimento:  date
    numeroSUS: str
    idPaciente: str  
    sexo : str
    info: str
    micro: int

    class Config:
        orm_mode = True

class PacienteOut(BaseModel):
    dataNascimento:  date
    numeroSUS: str
    idPaciente: str  
    sexo : str
    info: str
    micro: int

    class Config:
        orm_mode = True

class PessoaOut(BaseModel):
    cpf: str
    nome: str
    email: str
    micro: int
    class Config:
        orm_mode = True

class PacienteWithPessoaOut(BaseModel):
    numeroSUS: str
    idPaciente: str
    dataNascimento: Optional[date]  # ou Date
    sexo: Optional[str]
    info: Optional[str]
    pessoa: PessoaOut
    micro: int
    class Config:
        orm_mode = True

class ConsultaOut(BaseModel):
    id: int  
    idPaciente: str  
    idFuncionario: str  
    data: date
    dataRetorno: date  
    hbg: Optional[float] = None  
    tomaMedHipertensao: Optional[str] = None  
    praticaAtivFisica: Optional[str] = None  
    imc: Optional[float] = None  
    peso: Optional[float] = None  
    historicoAcucarElevado: Optional[str] = None  
    altura: Optional[float] = None  
    cintura: Optional[float] = None  
    resultadoFindRisc: Optional[str] = None  
    frequenciaIngestaoVegetaisFrutas: Optional[str] = None  
    class Config:
        orm_mode = True


class PacienteSchema(BaseModel):
    numeroSUS: str
    dataNascimento: Optional[date]
    sexo: Optional[str]
    info: Optional[str]
    cpf: str
    nome: str
    email: str
    micro: int
    class Config:
        orm_mode = True

class ConsultaSchema(BaseModel):
    id: int
    idFuncionario: str
    data: date
    dataRetorno: Optional[date]  # Campo adicional, certifique-se de que existe no modelo
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
    historicoFamiliar: Optional[str]  # Campo adicional, certifique-se de que existe no modelo
    medico: Optional[str]  # Campo adicional, certifique-se de que existe no modelo

    class Config:
        orm_mode = True

class PacienteWithPessoaConsultaOut(BaseModel):
    paciente: PacienteSchema
    consultas: List[ConsultaSchema]

    class Config:
        orm_mode = True

