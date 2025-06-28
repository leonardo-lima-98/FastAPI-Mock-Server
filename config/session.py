from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config import settings
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname

# Cria o engine async com o banco
engine = create_engine(url=settings.DATABASE_URL, echo=True)

# Dependência para usar em rotas
def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
