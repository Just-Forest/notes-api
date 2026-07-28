from pydantic import Field

from src import BaseSchema


class NotesPostSchema(BaseSchema):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)
