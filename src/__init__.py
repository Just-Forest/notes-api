from pydantic import Field
from typing import Annotated, Literal

from src.api.schemas.base import BaseSchema


class HealthResponse(BaseSchema):
    status: Annotated[Literal["healthy"], Field()]