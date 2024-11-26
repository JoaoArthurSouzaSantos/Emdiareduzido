from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from depends import get_db_session, token_verifier
from .auth_funcionario import FuncionarioUseCases
from .schemas import FuncionarioSchema,FuncionarioLogin
from fastapi import HTTPException
from .auth_funcionario import crypt_context
from .models import FuncionarioModel

funcionario_router = APIRouter()
test_router = APIRouter(prefix='/test ', dependencies=[Depends(token_verifier)])


@funcionario_router.post('/register')
def funcionario_register(
    funcionario: FuncionarioSchema,
    db_session: Session = Depends(get_db_session),
):
    uc = FuncionarioUseCases(db_session=db_session)
    uc.funcionario_register(funcionario=funcionario)
    return JSONResponse(
        content={'msg': 'success'},
        status_code=status.HTTP_201_CREATED
    )


@funcionario_router.post('/login')
def funcionario_register(
    request_form_funcionario: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(get_db_session),
):
    uc = FuncionarioUseCases(db_session=db_session)
    funcionario = FuncionarioLogin(
        username=request_form_funcionario.username,
        password=request_form_funcionario.password
    )

    auth_data = uc.funcionario_login(funcionario=funcionario)
    return JSONResponse(
        content=auth_data,
        status_code=status.HTTP_200_OK
    )

@funcionario_router.put('/{id}')
def editar_funcionario(
    id: int,  # O ID do funcionário a ser editado
    funcionario: FuncionarioSchema,  # Dados atualizados do funcionário
    db_session: Session = Depends(get_db_session),
    current_user: str = Depends(token_verifier),  # Token é verificado aqui
):
    uc = FuncionarioUseCases(db_session=db_session)
    # Verifica se o funcionário existe
    funcionario_on_db = db_session.query(FuncionarioModel).filter_by(id=id).first()
    
    if not funcionario_on_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionario not found"
        )

    # Se a senha for alterada, criptografamos a nova senha
    if funcionario.password:
        funcionario_on_db.password = crypt_context.hash(funcionario.password)

    funcionario_on_db.username = funcionario.username  # Atualiza o nome de usuário

    try:
        db_session.commit()  # Comita as alterações no banco de dados
        return JSONResponse(
            content={'msg': 'Funcionario updated successfully'},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        db_session.rollback()  # Caso haja erro, faz o rollback
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error updating funcionario"
        )

@funcionario_router.delete('/{id}')
def excluir_funcionario(
    id: int,  # O ID do funcionário a ser excluído
    db_session: Session = Depends(get_db_session),
    current_user: str = Depends(token_verifier),  # Token é verificado aqui
):
    uc = FuncionarioUseCases(db_session=db_session)
    # Verifica se o funcionário existe
    funcionario_on_db = db_session.query(FuncionarioModel).filter_by(id=id).first()

    if not funcionario_on_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionario not found"
        )

    # Deleta o funcionário
    try:
        db_session.delete(funcionario_on_db)
        db_session.commit()
        return JSONResponse(
            content={'msg': 'Funcionario deleted successfully'},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        db_session.rollback()  # Caso haja erro, faz o rollback
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error deleting funcionario"
        )



@test_router.get('/test')
def test_user_verify():
    return 'It works'
