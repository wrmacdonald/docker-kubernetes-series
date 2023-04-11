from sqlmodel import create_engine

SQL_DATABASE_NAME=""
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@host.docker.internal:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)