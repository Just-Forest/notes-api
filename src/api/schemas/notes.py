from pydantic import Field

from src.api.schemas.base import BaseSchema


class NotesPostSchema(BaseSchema):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class NoteItem(BaseSchema):
    id: int
    title: str
    content: str


class GetAllNotes(BaseSchema):
    all_notes: list[NoteItem]


class UpdatedNotes(BaseSchema):
    success: bool
    updated_rows: int
