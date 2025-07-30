from pydantic import BaseModel


class Note(BaseModel):
    id: int
    text: str
    is_completed: bool


class NoteCreate(BaseModel):
    text: str


class NoteRead(BaseModel):
    id: int
    text: str
    is_completed: bool
