from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import SQLModel, Field


class PastesCreate(SQLModel):
    input: str
    language: str
    ttl: int


class Pastes(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None, unique=True)
    code: str | None = Field(default=None, unique=True)
    input: str
    language: str
    ttl: int
    creation_time: datetime = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    )
    expiration_time: datetime | None = Field(default=None, sa_column=Column(TIMESTAMP(timezone=True)))
