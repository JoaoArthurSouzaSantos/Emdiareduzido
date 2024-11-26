from datetime import datetime, timedelta
from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config
from .models import FuncionarioModel
from .schemas import FuncionarioSchema


SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

crypt_context = CryptContext(schemes=['sha256_crypt'])


class FuncionarioUseCases:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def funcionario_register(self, funcionario: FuncionarioSchema):
        funcionario_model = FuncionarioModel(
            username=funcionario.username,
            password=crypt_context.hash(funcionario.password),
            id = funcionario.id
        )
        try:
            self.db_session.add(funcionario_model)
            self.db_session.commit()
        except Exception as error:
            print(error)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Funcionario already exists'
            )

    def funcionario_login(self, funcionario: FuncionarioSchema, expires_in: int = 30):
        funcionario_on_db = self.db_session.query(FuncionarioModel).filter_by(username=funcionario.username).first()

        if funcionario_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        if not crypt_context.verify(funcionario.password, funcionario_on_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
        
        exp = datetime.utcnow() + timedelta(minutes=expires_in)

        payload = {
            'sub': funcionario.username,
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }

    def verify_token(self, access_token):
        try:
            data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
        
        funcionario_on_db = self.db_session.query(FuncionarioModel).filter_by(username=data['sub']).first()

        if funcionario_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid access token'
            )
