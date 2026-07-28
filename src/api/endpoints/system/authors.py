from typing import Annotated

from authx import TokenPayload
from fastapi import HTTPException, Depends, APIRouter
from pwdlib import PasswordHash
from sqlalchemy import select, update, delete

from src.api.endpoints.dependencies import get_current_user
from src.api.schemas.notes import NotesPostSchema, GetAllNotes, UpdatedNotes
from src.api.schemas.users import UserLoginSchema, LoginResponse
from src.database import session_factory
from src.database.note import Note
from src.database.user import User
from src.security import security

router = APIRouter()

password_hash = PasswordHash.recommended()


@router.post("/login", response_model=LoginResponse)
def login(creds: UserLoginSchema):
    stmt = select(User).where(User.name == creds.name)
    with session_factory() as session:
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
def signup(creds: UserLoginSchema):
    stmt = select(User).where(User.name == creds.name)
    with session_factory() as session:
        user = session.execute(stmt).scalars().first()
        if user is not None:
            raise HTTPException(
                status_code=409, detail="User with this name already exists"
            )
        hashed_password = password_hash.hash(creds.password)
        user = User(name=creds.name, password=hashed_password)
        session.add(user)
        session.commit()
    return {"success": True}


@router.get("/notes", response_model=GetAllNotes)
def get_all_notes(
        current_user: Annotated[User, Depends(get_current_user)]
):
    with session_factory() as session:
        stmt = select(Note).where(Note.user_id == current_user.id)
        notes = session.execute(stmt).scalars().all()
        return {
            "all_notes": [
                {
                    "id": note.id,
                    "title": note.title,
                    "content": note.content
                }
                for note in notes
            ]
        }


@router.post("/notes")
def add_note(creds: NotesPostSchema,
             current_user: Annotated[User, Depends(get_current_user)]
             ):
    with session_factory() as session:
        note = Note(title=creds.title,
                    content=creds.content,
                    user_id=current_user.id
                    )
        session.add(note)
        session.commit()
    return {"success": True}


@router.put("/notes/{note_id}", response_model=UpdatedNotes)
def update_note(creds: NotesPostSchema,
                current_user: Annotated[User, Depends(get_current_user)],
                note_id: int
                ):
    with session_factory() as session:
        stmt = (
            update(Note)
            .where(Note.id == note_id, Note.user_id == current_user.id)
            .values(title=creds.title, content=creds.content)
        )
        result = session.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Note not found",
            )
        session.commit()
        return {
            "success": True,
            "updated_rows": result.rowcount,
        }


@router.delete("/notes/{note_id}", response_model=UpdatedNotes)
def delete_note(
        current_user: Annotated[User, Depends(get_current_user)],
        note_id: int
):
    with session_factory() as session:
        stmt = (
            delete(Note)
            .where(Note.id == note_id, Note.user_id == current_user.id)
        )
        result = session.execute(stmt)
        if result.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Note not found",
            )
        session.commit()
        return {
            "success": True,
            "updated_rows": result.rowcount,
        }


@router.get("/protected")
def protected(
        payload: Annotated[TokenPayload, Depends(security.access_token_required)]
):
    return payload
