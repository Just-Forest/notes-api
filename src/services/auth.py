from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database.user import User
from src.security import security
from src.services.exceptions import InvalidCredentials, AlreadyExists

password_hash = PasswordHash.recommended()


class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def login(self, name: str, password: str) -> dict[str, str]:
        stmt = select(User).where(User.name == name)
        user = self.session.execute(stmt).scalars().first()
        if user is None or not password_hash.verify(password, user.password):
            raise InvalidCredentials("Incorrect name or password")
        return {
            "access_token": security.create_access_token(uid=str(user.id)),
            "refresh_token": security.create_refresh_token(uid=str(user.id)),
        }

    def signup(self, name, password):
        stmt = select(User).where(User.name == name)
        user = self.session.execute(stmt).scalars().first()
        if user is not None:
            raise AlreadyExists("User with this name already exists")
        hashed_password = password_hash.hash(password)
        user = User(name=name, password=hashed_password)
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise AlreadyExists("User with this name already exists")
        return {"success": True}
