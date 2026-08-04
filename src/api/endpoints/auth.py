from typing import Annotated

from authx import TokenPayload
from fastapi import Depends, APIRouter, status

from src.security import security
from src.api.schemas.users import UserLoginSchema, RefreshResponse, TokenPair
from src.api.dependencies import get_auth_service
from src.services.auth import AuthService

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=TokenPair)
def login(
    creds: UserLoginSchema,
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    return service.login(creds.name, creds.password)


@router.post("/signup", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
def signup(
    creds: UserLoginSchema, service: Annotated[AuthService, Depends(get_auth_service)]
):
    return service.signup(creds.name, creds.password)


@router.post("/refresh", response_model=RefreshResponse)
def refresh(
    payload: Annotated[TokenPayload, Depends(security.refresh_token_required)],
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    return service.refresh(int(payload.sub))
