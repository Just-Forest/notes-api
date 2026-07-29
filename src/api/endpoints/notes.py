from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from src.api.dependencies import get_current_user
from src.api.schemas.notes import GetAllNotes, NoteItem, NotesPostSchema, UpdatedNotes
from src.database.note import Note
from src.database.session import get_session
from src.database.user import User

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=GetAllNotes)
def get_all_notes(
        current_user: Annotated[User, Depends(get_current_user)],
        session: Annotated[Session, Depends(get_session)]
):
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


@router.post("", response_model=NoteItem)
def add_note(creds: NotesPostSchema,
             current_user: Annotated[User, Depends(get_current_user)],
             session: Annotated[Session, Depends(get_session)]
             ):
    note = Note(title=creds.title,
                content=creds.content,
                user_id=current_user.id
                )
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


@router.put("/{note_id}", response_model=UpdatedNotes)
def update_note(creds: NotesPostSchema,
                current_user: Annotated[User, Depends(get_current_user)],
                note_id: int,
                session: Annotated[Session, Depends(get_session)]
                ):
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


@router.delete("/{note_id}", response_model=UpdatedNotes)
def delete_note(
        current_user: Annotated[User, Depends(get_current_user)],
        note_id: int,
        session: Annotated[Session, Depends(get_session)]
):
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
