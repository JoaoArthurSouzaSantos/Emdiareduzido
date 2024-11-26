from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class FuncionarioModel(Base):
    __tablename__ = "funcionarios"
    id = Column(String(255), ForeignKey('pessoas.cpf'), primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255), index=True)

    pessoa = relationship("Pessoa", back_populates="funcionario")
    consultas = relationship("Consulta", back_populates="funcionario", cascade="all, delete-orphan")
