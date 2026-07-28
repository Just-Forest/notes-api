from typing import Annotated, Literal

from pydantic import Field, BaseModel, ConfigDict

from src.api.schemas.base import BaseSchema


class HealthResponse(BaseSchema):
    status: Annotated[Literal["healthy"], Field()]


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
