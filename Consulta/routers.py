from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from shared.dependencies import get_db
from .models import Consulta
from .schemas import ConsultaCreate, ConsultaOut
from typing import List
from datetime import date

router = APIRouter()

@router.post("/consulta/", response_model=ConsultaOut)
def create_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db)):
    db_consulta = Consulta(**consulta.dict())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@router.get("/consulta/{consulta_id}", response_model=ConsultaOut)
def read_consulta(consulta_id: int, db: Session = Depends(get_db)):
    db_consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta not found")
    return db_consulta

@router.put("/consulta/{consulta_id}", response_model=ConsultaOut)
def update_consulta(consulta_id: int, consulta: ConsultaCreate, db: Session = Depends(get_db)):
    db_consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta not found")
    for key, value in consulta.dict().items():
        setattr(db_consulta, key, value)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

@router.delete("/consulta/{consulta_id}")
def delete_consulta(consulta_id: int, db: Session = Depends(get_db)):
    db_consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if db_consulta is None:
        raise HTTPException(status_code=404, detail="Consulta not found")
    db.delete(db_consulta)
    db.commit()
    return {"message": "Consulta deleted successfully"}

# Histórico de consultas
@router.get("/relatorio/historico", response_model=List[ConsultaOut])
def get_historico_consultas(db: Session = Depends(get_db)):
    consultas = db.query(Consulta).all()
    return consultas

# Consultas dentro de uma data escolhida
@router.get("/relatorio/data", response_model=List[ConsultaOut])
def get_consultas_por_data(data_escolhida: date, db: Session = Depends(get_db)):
    consultas = db.query(Consulta).filter(Consulta.data == data_escolhida).all()
    return consultas

# Consultas feitas por um funcionário específico
@router.get("/relatorio/funcionario/{id_funcionario}", response_model=List[ConsultaOut])
def get_consultas_por_funcionario(id_funcionario: int, db: Session = Depends(get_db)):
    consultas = db.query(Consulta).filter(Consulta.id_funcionario == id_funcionario).all()
    return consultas

# Consultas de um paciente específico
@router.get("/relatorio/paciente/{id_paciente}", response_model=List[ConsultaOut])
def get_consultas_por_paciente(id_paciente: int, db: Session = Depends(get_db)):
    consultas = db.query(Consulta).filter(Consulta.id_paciente == id_paciente).all()
    return consultas

# Consultas entre duas datas específicas
@router.get("/relatorio/periodo", response_model=List[ConsultaOut])
def get_consultas_por_periodo(data_inicio: date, data_fim: date, db: Session = Depends(get_db)):
    consultas = db.query(Consulta).filter(and_(Consulta.data >= data_inicio, Consulta.data <= data_fim)).all()
    return consultas

# Número de consultas por dia
@router.get("/relatorio/consultas_por_dia", response_model=List[dict])
def get_numero_consultas_por_dia(db: Session = Depends(get_db)):
    consultas = db.query(Consulta.data, func.count(Consulta.id).label('count')).group_by(Consulta.data).all()
    return [{"data": dia, "count": count} for dia, count in consultas]

# Relatório de consultas futuras
@router.get("/relatorio/futuros", response_model=List[ConsultaOut])
def get_consultas_futuras(db: Session = Depends(get_db)):
    today = date.today()
    consultas = db.query(Consulta).filter(Consulta.data >= today).all()
    return consultas
