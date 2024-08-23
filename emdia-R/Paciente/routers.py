from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from Paciente.models import Paciente
from Paciente.schemas import PacienteCreate, PacienteOut ,PacienteWithPessoaOut
from Pessoa.models import Pessoa
from Consulta.models import Consulta

router = APIRouter()
#rota para extrair tds os dados da mesma entidade
#rota para tds as consulta desse paciente 
#rotas para tds os valores de Hemoglobina g e data

# @router.get("/paciente_consultas/{numeroSUS}", response_model=PacienteWithConsultasOut)
# def get_paciente_with_consultas(numeroSUS: str, db: Session = Depends(get_db)):
#     paciente = db.query(Paciente).filter(Paciente.numeroSUS == numeroSUS).first()
    
#     if paciente is None:
#         raise HTTPException(status_code=404, detail="Paciente não encontrado")

#     consultas = db.query(Consulta).filter(Consulta.id_paciente == numeroSUS).all()
    
#     paciente.consultas = consultas
#     return paciente

@router.get("/paciente_pessoa/{numeroSUS}", response_model=PacienteWithPessoaOut)
def get_paciente_with_pessoa(numeroSUS: str, db: Session = Depends(get_db)):
    # Realizando a consulta para buscar o Paciente e a Pessoa associada
    paciente_pessoa = (
        db.query(Paciente)
        .join(Pessoa, Paciente.id_paciente == Pessoa.cpf)
        .filter(Paciente.numeroSUS == numeroSUS)
        .first()
    )
    
    if paciente_pessoa is None:
        raise HTTPException(status_code=404, detail="Paciente ou Pessoa não encontrados")
    
    return paciente_pessoa

@router.post("/create/", response_model=PacienteOut)
def create_paciente(paciente_create: PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = Paciente(**paciente_create.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@router.get("/read/{numeroSUS}", response_model=PacienteOut)
def read_paciente(numeroSUS: str, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.numeroSUS == numeroSUS).first()
    if paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

@router.put("/update/{numeroSUS}", response_model=PacienteOut)
def update_paciente(numeroSUS: str, paciente_update: PacienteCreate, db: Session = Depends(get_db)):
    db_paciente = db.query(Paciente).filter(Paciente.numeroSUS == numeroSUS).first()
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    for field, value in paciente_update.dict(exclude_unset=True).items():
        setattr(db_paciente, field, value)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@router.delete("/delete/{numeroSUS}", response_model=PacienteOut)
def delete_paciente(numeroSUS: str, db: Session = Depends(get_db)):
    db_paciente = db.query(Paciente).filter(Paciente.numeroSUS == numeroSUS).first()
    if db_paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db.delete(db_paciente)
    db.commit()
    return db_paciente
