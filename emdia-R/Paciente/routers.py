from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from Paciente.models import Paciente
from Paciente.schemas import PacienteCreate, PacienteOut ,PacienteWithPessoaOut,PacienteWithPessoaConsultaOut
from Pessoa.models import Pessoa
from Consulta.models import Consulta
from sqlalchemy.exc import IntegrityError

router = APIRouter()
#rota para extrair tds os dados da mesma entidade
#rota para tds as consulta desse paciente 
@router.get("/paciente_pessoa_consulta/{numeroSUS}", response_model=PacienteWithPessoaConsultaOut)
def get_paciente_pessoa_consulta(numeroSUS: str, db: Session = Depends(get_db)):
    # Buscar o paciente, pessoa e consultas associadas
    paciente_pessoa_consulta = (
        db.query(Paciente)
        .join(Pessoa, Paciente.idPaciente == Pessoa.cpf)
        .outerjoin(Consulta, Paciente.numeroSUS == Consulta.idPaciente)
        .filter(Paciente.numeroSUS == numeroSUS)
        .first()
    )
    
    if paciente_pessoa_consulta is None:
        raise HTTPException(status_code=404, detail="Paciente, Pessoa ou Consulta não encontrados")

    # Montar o retorno no formato solicitado
    resultado = {
        "paciente": {
            "numeroSUS": paciente_pessoa_consulta.numeroSUS,
            "dataNascimento": paciente_pessoa_consulta.data_nascimento,
            "sexo": paciente_pessoa_consulta.sexo,
            "info": paciente_pessoa_consulta.info,
            "cpf": paciente_pessoa_consulta.pessoa.cpf,
            "nome": paciente_pessoa_consulta.pessoa.nome,
            "email": paciente_pessoa_consulta.pessoa.email,
        },
        "consultas": [
            {
                "id": consulta.id,
                "idFuncionario": consulta.id_funcionario,
                "data": consulta.data,
                "dataRetorno": consulta.dataretorno,  # Certifique-se de que este campo existe no modelo de consulta
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
                "historicoFamiliar": consulta.historicoFamiliar,  # Certifique-se de que este campo existe no modelo
                "medico": consulta.medico  # Certifique-se de que este campo existe no modelo
            } for consulta in paciente_pessoa_consulta.consultas
        ]
    }
    
    return resultado



@router.get("/paciente_pessoa/{numeroSUS}", response_model=PacienteWithPessoaOut)
def get_paciente_with_pessoa(numeroSUS: str, db: Session = Depends(get_db)):
    # Realizando a consulta para buscar o Paciente e a Pessoa associada
    paciente_pessoa = (
        db.query(Paciente, Pessoa)
        .join(Pessoa, Paciente.idPaciente == Pessoa.cpf)
        .filter(Paciente.numeroSUS == numeroSUS)
        .first()
    )
    
    if paciente_pessoa is None:
        raise HTTPException(status_code=404, detail="Paciente ou Pessoa não encontrados")
    
    paciente, pessoa = paciente_pessoa
    
    return {
        "numeroSUS": paciente.numeroSUS,
        "idPaciente": paciente.iPaciente,
        "dataNascimento": paciente.dataNascimento,
        "sexo": paciente.sexo,
        "info": paciente.info,
        "pessoa": {
            "cpf": pessoa.cpf,
            "nome": pessoa.nome,
            "email": pessoa.email
        }
    }


@router.post("/create/", response_model=PacienteOut)
def create_paciente(paciente_create: PacienteCreate, db: Session = Depends(get_db)):
    # Verificar se o CPF já está cadastrado
    paciente_existente = db.query(Paciente).filter(Paciente.numeroSUS == paciente_create.numeroSUS).first()
    if paciente_existente:
        raise HTTPException(status_code=400, detail="Paciente com o número SUS já existe")
    
    try:
        # Criar e adicionar o novo paciente
        db_paciente = Paciente(**paciente_create.dict())
        db.add(db_paciente)
        db.commit()
        db.refresh(db_paciente)
        return db_paciente
    except IntegrityError:
        # Em caso de erro de integridade, como violação de chave única
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro de integridade ao criar o paciente")

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
