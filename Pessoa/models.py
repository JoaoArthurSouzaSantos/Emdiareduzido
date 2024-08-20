from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from shared.database import Base

class Pessoa(Base):
    __tablename__ = "pessoas"
    
    cpf = Column(String(255), primary_key=True, index=True)  
    nome = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)

    
    paciente = relationship("Paciente", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    funcionario = relationship("Funcionario", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
