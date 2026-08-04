from pydantic import field_validator, ConfigDict, Field

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


class LoginResponse(BaseSchema):
    model_config = ConfigDict(populate_by_name=True)
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class RefreshResponse(BaseSchema):
    access_token: str
