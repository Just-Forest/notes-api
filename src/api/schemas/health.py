from typing import Annotated, Literal
from pydantic import Field

from src.api.schemas.base import BaseSchema


class HealthResponse(BaseSchema):
    status: Annotated[Literal["healthy"], Field()]
