from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Pessoa.models import Pessoa
from Pessoa.schemas import PessoaCreate, PessoaOut
from shared.dependencies import get_db

router = APIRouter()

@router.post("/create/", response_model=PessoaOut)
def create_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db)):
    db_pessoa = Pessoa(**pessoa.dict())
    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

@router.get("/read/{cpf}", response_model=PessoaOut)
def read_pessoa(cpf: str, db: Session = Depends(get_db)):
    pessoa = db.query(Pessoa).filter(Pessoa.cpf == cpf).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return pessoa

@router.put("/update/{cpf}", response_model=PessoaOut)
def update_pessoa(cpf: str, pessoa: PessoaCreate, db: Session = Depends(get_db)):
    db_pessoa = db.query(Pessoa).filter(Pessoa.cpf == cpf).first()
    if not db_pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    for key, value in pessoa.dict().items():
        setattr(db_pessoa, key, value)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

@router.delete("/delete/{cpf}", response_model=PessoaOut)
def delete_pessoa(cpf: str, db: Session = Depends(get_db)):
    db_pessoa = db.query(Pessoa).filter(Pessoa.cpf == cpf).first()
    if not db_pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    db.delete(db_pessoa)
    db.commit()
    return db_pessoa
