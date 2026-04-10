from sqlmodel import SQLModel


class PastesCreate(SQLModel):
    pass


class Urls(SQLModel, table=True):
    pass
