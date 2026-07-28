from pydantic import Field, ConfigDict

from src import BaseSchema


class NotesPostSchema(BaseSchema):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class GetAllNotes(BaseSchema):
    model_config = ConfigDict(populate_by_name=True)
    id: int
    title: str
    content: str


class UpdatedNotes(BaseSchema):
    success: bool
    updated_rows: int
