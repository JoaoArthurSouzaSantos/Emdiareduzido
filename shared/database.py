from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# URL de conexão para MySQL com usuário root e senha vazia
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost:3306/emdia"

# Criar o engine do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Criar uma instância do objeto SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Usar declarative_base diretamente do módulo sqlalchemy.orm
Base = declarative_base()
