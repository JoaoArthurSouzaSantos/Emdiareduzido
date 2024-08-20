from sqlalchemy import Column, Integer, String , Date , ForeignKey
from sqlalchemy.orm import relationship
from shared.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    numeroSUS = Column(Integer, primary_key=True, index=True)  # Número SUS como chave primária
    id_paciente = Column(String(255), ForeignKey('pessoas.cpf'), index=True)  # Chave estrangeira referenciando o CPF na tabela pessoas
    data_nascimento = Column(Date)
    sexo = Column(String(255), index=True)
    info = Column(String(255), index=True)
    # Define a relationship to the Pessoa table based on the id_pessoa foreign key
    pessoa = relationship("Pessoa", back_populates="paciente")
    consultas = relationship("Consulta", back_populates="paciente")

