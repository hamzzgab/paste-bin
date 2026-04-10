from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine

from app.config import settings

DATABASE_URL = (f'postgresql://{settings.database_username}:{settings.database_password}'
                f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


SessionDep: type[Session] = Annotated[Session, Depends(get_session)]
