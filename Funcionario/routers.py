from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from Funcionario.models import Funcionario
from Funcionario.schemas import FuncionarioCreate, FuncionarioOut

router = APIRouter()

@router.post("/create/", response_model=FuncionarioOut)
def create_funcionario(funcionario_create: FuncionarioCreate, db: Session = Depends(get_db)):
    db_funcionario = Funcionario(**funcionario_create.dict())
    db.add(db_funcionario)
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

@router.get("/read/{id}", response_model=FuncionarioOut)
def read_funcionario(id: str, db: Session = Depends(get_db)):
    funcionario = db.query(Funcionario).filter(Funcionario.id == id).first()
    if funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@router.put("/update/{id}", response_model=FuncionarioOut)
def update_funcionario(id: str, funcionario_update: FuncionarioCreate, db: Session = Depends(get_db)):
    db_funcionario = db.query(Funcionario).filter(Funcionario.id == id).first()
    if db_funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    for field, value in funcionario_update.dict(exclude_unset=True).items():
        setattr(db_funcionario, field, value)
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

@router.delete("/delete/{id}", response_model=FuncionarioOut)
def delete_funcionario(id: str, db: Session = Depends(get_db)):
    db_funcionario = db.query(Funcionario).filter(Funcionario.id == id).first()
    if db_funcionario is None:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    db.delete(db_funcionario)
    db.commit()
    return db_funcionario
