from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pessoa.models import Pessoa
from pessoa.schemas import PessoaCreate, PessoaOut
from depends import get_db_session, token_verifier  # Importa o verificador de token

router = APIRouter()

# Rota aberta (não protegida)
@router.post("/create/", response_model=PessoaOut)
def create_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db_session)):
    # Verifica se já existe uma pessoa com o CPF
    existing_pessoa = db.query(Pessoa).filter(Pessoa.cpf == pessoa.cpf).first()
    if existing_pessoa:
        raise HTTPException(status_code=400, detail="Pessoa com esse CPF já existe")
    
    db_pessoa = Pessoa(**pessoa.dict())
    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

# Rota protegida
@router.get("/read/{cpf}", response_model=PessoaOut, dependencies=[Depends(token_verifier)])
def read_pessoa(cpf: str, db: Session = Depends(get_db_session)):
    pessoa = db.query(Pessoa).filter(Pessoa.cpf == cpf).first()
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return pessoa

# Rota protegida
@router.put("/update/{cpf}", response_model=PessoaOut, dependencies=[Depends(token_verifier)])
def update_pessoa(cpf: str, pessoa: PessoaCreate, db: Session = Depends(get_db_session)):
    db_pessoa = db.query(Pessoa).filter(Pessoa.cpf == cpf).first()
    if not db_pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    for key, value in pessoa.dict().items():
        setattr(db_pessoa, key, value)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

# Rota protegida
@router.delete("/delete/{cpf}", response_model=PessoaOut, dependencies=[Depends(token_verifier)])
def delete_pessoa(cpf: str, db: Session = Depends(get_db_session)):
    db_pessoa = db.query(Pessoa).filter(Pessoa.cpf == cpf).first()
    if not db_pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    db.delete(db_pessoa)
    db.commit()
    return db_pessoa
