from typing import Annotated

from fastapi import Depends, APIRouter


from src.api.schemas.users import LoginResponse, UserLoginSchema
from src.api.dependencies import get_auth_service
from src.services.auth import AuthService

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    creds: UserLoginSchema,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    return service.login(creds.name, creds.password)


@router.post("/signup")
def signup(
    creds: UserLoginSchema, service: Annotated[AuthService, Depends(get_auth_service)]
):
    return service.signup(creds.name, creds.password)
