from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from src.api.schemas.users import LoginResponse, UserLoginSchema
from src.database.session import get_session
from src.database.user import User
from src.security import security

password_hash = PasswordHash.recommended()
# top of auth.py
router = APIRouter(tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(creds: UserLoginSchema,
          session: Annotated[Session, Depends(get_session)]
          ):
    stmt = select(User).where(User.name == creds.name)
    user = session.execute(stmt).scalars().first()
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect name or password")
    if password_hash.verify(creds.password, user.password):
        access_token = security.create_access_token(uid=str(user.id))
        refresh_token = security.create_refresh_token(uid=str(user.id))
        return {"access_token": access_token,
                "refresh_token": refresh_token}
    raise HTTPException(status_code=401, detail="Incorrect name or password")


@router.post("/signup")
def signup(creds: UserLoginSchema,
           session: Annotated[Session, Depends(get_session)]
           ):
    stmt = select(User).where(User.name == creds.name)
    user = session.execute(stmt).scalars().first()
    if user is not None:
        raise HTTPException(
            status_code=409, detail="User with this name already exists"
        )
    hashed_password = password_hash.hash(creds.password)
    user = User(name=creds.name, password=hashed_password)
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409, detail="User with this name already exists"
        )
    return {"success": True}