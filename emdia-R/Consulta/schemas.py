from pydantic import BaseModel
from datetime import date
from typing import Optional

class ConsultaCreate(BaseModel):
    id_paciente: int  
    id_funcionario: str  
    data: date  
    dataretorno: date  # Certifique-se de que este nome corresponde ao nome do campo no SQLAlchemy
    hbg: Optional[float] = None  
    tomaMedHipertensao: Optional[str] = None  
    praticaAtivFisica: Optional[str] = None  
    imc: Optional[float] = None  
    peso: Optional[float] = None  
    historicoAcucarElevado: Optional[str] = None  
    altura: Optional[float] = None  
    cintura: Optional[float] = None  
    resultadoFindRisc: Optional[str] = None  
    historicoFamiliar: Optional[str] = None
    frequenciaIngestaoVegetaisFrutas: Optional[str] = None  
    medico: Optional[str] = None  
    class Config:
        orm_mode = True

class ConsultaOut(BaseModel):
    id: int  
    id_paciente: int 
    id_funcionario: str  
    data: date  
    dataretorno: date  # Altere este nome para corresponder ao nome do campo no SQLAlchemy
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
    historicoFamiliar: Optional[str] = None
    medico: Optional[str] = None  
    class Config:
        orm_mode = True


class ConsultaPacientePessoaOut(BaseModel):
    id: int
    id_paciente: str
    id_funcionario: str
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
    historicoFamiliar: Optional[str] = None
    medico: Optional[str] = None
    
    numeroSUS: str
    data_nascimento: date
    sexo: str
    info: str
    cpf: str
    nome: str
    email: str

    class Config:
        orm_mode = True

from pydantic import BaseModel
from typing import Optional
from datetime import date

class EvolucaoHB(BaseModel):
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
    historicoFamiliar: Optional[str] = None
    medico: Optional[str] = None
    data_nascimento: date
    sexo: str
    info: str
    nome: str

    class Config:
        orm_mode = True
