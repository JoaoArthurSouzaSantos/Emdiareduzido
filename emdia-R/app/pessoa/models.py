from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from db.base import Base

class Pessoa(Base):
    __tablename__ = "pessoas"
    
    cpf = Column(String(255), primary_key=True, index=True)  
    nome = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)

    # Alterado para garantir que a classe Funcionario seja reconhecida
    paciente = relationship("Paciente", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
    funcionario = relationship("FuncionarioModel", back_populates="pessoa", uselist=False, cascade="all, delete-orphan")
