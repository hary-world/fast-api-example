from sqlmodel import Field, SQLModel


class Note(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    text: str
    is_completed: bool = Field(default=False)


class NoteCreate(SQLModel):
    text: str


class NoteRead(SQLModel):
    id: int
    text: str
