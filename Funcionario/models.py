from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from shared.database import Base

class Funcionario(Base):
    __tablename__ = "funcionarios"
    id = Column(String(255), ForeignKey('pessoas.cpf'), primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255), index=True)

    # Relacionamentos
    pessoa = relationship("Pessoa", back_populates="funcionario")
    consultas = relationship("Consulta", back_populates="funcionario", cascade="all, delete-orphan")

