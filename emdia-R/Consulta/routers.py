from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_, func
from shared.dependencies import get_db
from .models import Consulta
from Paciente.models import Paciente
from Funcionario.models import Funcionario
from Pessoa.models import Pessoa
from .schemas import ConsultaCreate, ConsultaOut,ConsultaPacientePessoaOut,EvolucaoHB
from typing import List
from datetime import date

router = APIRouter()

@router.post("/consulta/", response_model=ConsultaCreate)
def create_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db)):
    # Verificar se o paciente existe
    paciente = db.query(Paciente).filter(Paciente.numeroSUS == consulta.id_paciente).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    # Verificar se o funcionário existe
    funcionario = db.query(Funcionario).filter(Funcionario.id == consulta.id_funcionario).first()
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")

    try:
        # Criar e adicionar a nova consulta
        db_consulta = Consulta(**consulta.dict())
        db.add(db_consulta)
        db.commit()
        db.refresh(db_consulta)
        return db_consulta
    except IntegrityError:
        # Em caso de erro de integridade, como chave estrangeira violada
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro de integridade ao criar a consulta")

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
    consultas = db.query(
        Consulta.id,
        Consulta.id_paciente,
        Pessoa.nome.label("nome"),  # Junta com a tabela Pessoa para pegar o nome
        Consulta.id_funcionario,
        Consulta.data,
        Consulta.dataretorno,
        Consulta.hbg,
        Consulta.tomaMedHipertensao,
        Consulta.praticaAtivFisica,
        Consulta.imc,
        Consulta.peso,
        Consulta.historicoAcucarElevado,
        Consulta.altura,
        Consulta.cintura,
        Consulta.resultadoFindRisc,
        Consulta.frequenciaIngestaoVegetaisFrutas,
        Consulta.historicoFamiliar,
        Consulta.medico
    ).join(Paciente, Paciente.numeroSUS == Consulta.id_paciente)\
     .join(Pessoa, Pessoa.cpf == Paciente.id_paciente)\
     .filter(Consulta.data == data_escolhida)\
     .all()

    return consultas

@router.get("/relatorio/funcionario/{id_funcionario}", response_model=List[ConsultaOut])
def get_consultas_por_funcionario(id_funcionario: int, db: Session = Depends(get_db)):
    consultas = db.query(
        Consulta.id,
        Consulta.id_paciente,
        Pessoa.nome.label("nome"),  # Junta com a tabela Pessoa para pegar o nome
        Consulta.id_funcionario,
        Consulta.data,
        Consulta.dataretorno,
        Consulta.hbg,
        Consulta.tomaMedHipertensao,
        Consulta.praticaAtivFisica,
        Consulta.imc,
        Consulta.peso,
        Consulta.historicoAcucarElevado,
        Consulta.altura,
        Consulta.cintura,
        Consulta.resultadoFindRisc,
        Consulta.frequenciaIngestaoVegetaisFrutas,
        Consulta.historicoFamiliar,
        Consulta.medico
    ).join(Paciente, Paciente.numeroSUS == Consulta.id_paciente)\
     .join(Pessoa, Pessoa.cpf == Paciente.id_paciente)\
     .filter(Consulta.id_funcionario == id_funcionario)\
     .all()

    return consultas


@router.get("/relatorio/paciente/{id_paciente}", response_model=List[ConsultaOut])
def get_consultas_por_paciente(id_paciente: int, db: Session = Depends(get_db)):
    consultas = db.query(
        Consulta.id,
        Consulta.id_paciente,
        Pessoa.nome.label("nome"),  # Junta com a tabela Pessoa para pegar o nome
        Consulta.id_funcionario,
        Consulta.data,
        Consulta.dataretorno,
        Consulta.hbg,
        Consulta.tomaMedHipertensao,
        Consulta.praticaAtivFisica,
        Consulta.imc,
        Consulta.peso,
        Consulta.historicoAcucarElevado,
        Consulta.altura,
        Consulta.cintura,
        Consulta.resultadoFindRisc,
        Consulta.frequenciaIngestaoVegetaisFrutas,
        Consulta.historicoFamiliar,
        Consulta.medico
    ).join(Paciente, Paciente.numeroSUS == Consulta.id_paciente)\
     .join(Pessoa, Pessoa.cpf == Paciente.id_paciente)\
     .filter(Consulta.id_paciente == id_paciente)\
     .all()

    return consultas



@router.get("/relatorio/periodo", response_model=List[ConsultaOut])
def get_consultas_por_periodo(data_inicio: date, data_fim: date, db: Session = Depends(get_db)):
    consultas = db.query(
        Consulta.id,
        Consulta.id_paciente,
        Consulta.id_funcionario,
        Consulta.data,
        Consulta.dataRetorno,
        Consulta.hbg,
        Consulta.tomaMedHipertensao,
        Consulta.praticaAtivFisica,
        Consulta.imc,
        Consulta.peso,
        Consulta.historicoAcucarElevado,
        Consulta.altura,
        Consulta.cintura,
        Consulta.resultadoFindRisc,
        Consulta.frequenciaIngestaoVegetaisFrutas,
        Consulta.historicoFamiliar,
        Consulta.medico,
        Pessoa.nome.label("nome")  # Pega o nome diretamente da tabela Pessoa
    ).join(Paciente, Paciente.numeroSUS == Consulta.id_paciente)\
     .join(Pessoa, Pessoa.cpf == Paciente.id_paciente)\
     .filter(and_(Consulta.data >= data_inicio, Consulta.data <= data_fim))\
     .all()

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



@router.get("/relatorio/paciente/pessoa/consultas_completo_da_pessoa{id_paciente}", response_model=List[ConsultaPacientePessoaOut])
def get_consultas_por_paciente(id_paciente: str, db: Session = Depends(get_db)):
    consultas = db.query(Consulta, Paciente, Pessoa).\
        join(Paciente, Consulta.id_paciente == Paciente.numeroSUS).\
        join(Pessoa, Paciente.id_paciente == Pessoa.cpf).\
        filter(Consulta.id_paciente == id_paciente).all()

    results = []
    for consulta, paciente, pessoa in consultas:
        results.append({
            "id": consulta.id,
            "id_paciente": consulta.id_paciente,
            "id_funcionario": consulta.id_funcionario,
            "data": consulta.data,
            "dataRetorno": consulta.dataRetorno,
            "hbg": consulta.hbg,
            "tomaMedHipertensao": consulta.tomaMedHipertensao,
            "praticaAtivFisica": consulta.praticaAtivFisica,
            "imc": consulta.imc,
            "peso": consulta.peso,
            "historicoAcucarElevado": consulta.historicoAcucarElevado,
            "altura": consulta.altura,
            "cintura": consulta.cintura,
            "resultadoFindRisc": consulta.resultadoFindRisc,
            "frequenciaIngestaoVegetaisFrutas": consulta.frequenciaIngestaoVegetaisFrutas,
            "historicoFamiliar": consulta.historicoFamiliar,
            "medico": consulta.medico,
            "numeroSUS": paciente.numeroSUS,
            "data_nascimento": paciente.data_nascimento,
            "sexo": paciente.sexo,
            "info": paciente.info,
            "cpf": pessoa.cpf,
            "nome": pessoa.nome,
            "email": pessoa.email
        })

    return results


@router.get("/relatorio/evoluçãoHB{id_paciente}", response_model=List[EvolucaoHB])
def get_consultas_por_paciente(id_paciente: str, db: Session = Depends(get_db)):
    consultas = db.query(Consulta, Paciente, Pessoa).\
        join(Paciente, Consulta.id_paciente == Paciente.numeroSUS).\
        join(Pessoa, Paciente.id_paciente == Pessoa.cpf).\
        filter(Consulta.id_paciente == id_paciente).all()

    results = []
    for consulta, paciente, pessoa in consultas:
        results.append({
            "data": consulta.data,
            "hbg": consulta.hbg,
            "tomaMedHipertensao": consulta.tomaMedHipertensao,
            "praticaAtivFisica": consulta.praticaAtivFisica,
            "imc": consulta.imc,
            "peso": consulta.peso,
            "historicoAcucarElevado": consulta.historicoAcucarElevado,
            "altura": consulta.altura,
            "cintura": consulta.cintura,
            "resultadoFindRisc": consulta.resultadoFindRisc,
            "frequenciaIngestaoVegetaisFrutas": consulta.frequenciaIngestaoVegetaisFrutas,
            "historicoFamiliar": consulta.historicoFamiliar,
            "medico": consulta.medico,
            "data_nascimento": paciente.data_nascimento,
            "sexo": paciente.sexo,
            "info": paciente.info,
            "nome": pessoa.nome,
        })

    return results