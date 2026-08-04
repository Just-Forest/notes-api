from pydantic import field_validator

from src.api.schemas.base import BaseSchema


class UserLoginSchema(BaseSchema):
    name: str
    password: str

    @field_validator("password", mode="after")
    @classmethod
    def validate_password(cls, value: str):
        if value.isalpha():
            raise ValueError("Password must include at least one number")
        if len(value) < 8:
            raise ValueError("Password must be >= 8")
        if value.isdigit():
            raise ValueError("Password must include at least one letter")
        if value.islower():
            raise ValueError("Password must have 1 upper letter")
        return value


class TokenPair(BaseSchema):
    access_token: str
    refresh_token: str


class RefreshResponse(BaseSchema):
    access_token: str
