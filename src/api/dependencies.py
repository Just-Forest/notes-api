from typing import Annotated

from authx import TokenPayload
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.session import get_session
from src.database.user import User
from src.security import security


def get_current_user(
    payload: Annotated[TokenPayload, Depends(security.access_token_required)],
    session: Annotated[Session, Depends(get_session)]
):
    user_id = int(payload.sub)
    stmt = select(User).where(User.id == user_id)
    user = session.execute(stmt).scalars().first()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )
    return user