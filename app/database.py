import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated

from fastapi import Depends
from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel import col, delete

from app.config import settings
from app.models import Pastes

DATABASE_URL = (f'postgresql://{settings.database_username}:{settings.database_password}'
                f'@{settings.database_hostname}:{settings.database_port}/{settings.database_name}')

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


async def cleanup_loop(interval_seconds: int = 5):
    while True:
        await asyncio.sleep(interval_seconds)
        with Session(engine) as session:
            session.exec(delete(Pastes)
                         .where(col(Pastes.expiration_time) < datetime.now(tz=timezone.utc)))
            session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    task = asyncio.create_task(cleanup_loop())
    yield
    task.cancel()


SessionDep: type[Session] = Annotated[Session, Depends(get_session)]
