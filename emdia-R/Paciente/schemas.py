from pydantic import BaseModel
from datetime import date
from typing import Optional
from typing import List

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

class ConsultaOut(BaseModel):
    id: int  
    id_paciente: int  
    id_funcionario: str  
    data: date  
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

class PacienteWithPessoaConsultaOut(BaseModel):
    numeroSUS: int
    id_paciente: str
    data_nascimento: Optional[date]
    sexo: Optional[str]
    info: Optional[str]
    pessoa: PessoaOut
    consultas: List[ConsultaOut]  # Lista de consultas

    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        # Serializa os dados corretamente, incluindo a lista de consultas
        return cls(
            numeroSUS=obj.numeroSUS,
            id_paciente=obj.id_paciente,
            data_nascimento=obj.data_nascimento.isoformat() if obj.data_nascimento else None,
            sexo=obj.sexo,
            info=obj.info,
            pessoa=obj.pessoa,
            consultas=[ConsultaOut.from_orm(c) for c in obj.consultas]
        )
    
