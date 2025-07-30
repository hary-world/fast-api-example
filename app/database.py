import os

from dotenv import load_dotenv
from sqlmodel import Field, Session, SQLModel, create_engine

load_dotenv(override=True)

engine = create_engine(os.getenv("DATABASE_URL"))


def get_db_session():
    with Session(engine) as session:
        yield session


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    is_completed: bool = Field(default=False)


class NoteCreate(SQLModel):
    text: str


class NoteRead(SQLModel):
    id: int
    text: str
