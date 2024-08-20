from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from shared.database import Base

class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    id_paciente = Column(Integer, ForeignKey('pacientes.numeroSUS'), index=True)
    id_funcionario = Column(String(255), ForeignKey('funcionarios.id'), index=True)
    data = Column(Date)
    hbg = Column(Float)
    tomaMedHipertensao = Column(String(255))
    praticaAtivFisica = Column(String(255))
    imc = Column(Float)
    peso = Column(Float)
    historicoAcucarElevado = Column(String(255))
    altura = Column(Float)
    cintura = Column(Float)
    resultadoFindRisc = Column(String(255))
    frequenciaIngestaoVegetaisFrutas = Column(String(255))
    historicoFamiliar  = Column(String(255))

    paciente = relationship("Paciente", back_populates="consultas")
    funcionario = relationship("Funcionario", back_populates="consultas")
