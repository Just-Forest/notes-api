from typing import Annotated

from fastapi import Depends, APIRouter

from src.api.dependencies import get_current_user, get_note_service
from src.api.schemas.notes import GetAllNotes, NoteItem, NotesPostSchema, UpdatedNotes
from src.database.user import User
from src.services.notes import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteItem)
def add_note(
    creds: NotesPostSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[NoteService, Depends(get_note_service)],
):
    return service.create(current_user.id, creds.title, creds.content)


@router.get("", response_model=GetAllNotes)
def get_all_notes(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[NoteService, Depends(get_note_service)],
):
    return {"all_notes": service.list_for_user(current_user.id)}


@router.put("/{note_id}", response_model=UpdatedNotes)
def update_note(
    creds: NotesPostSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[NoteService, Depends(get_note_service)],
    note_id: int,
):
    return {
        "success": True,
        "updated_rows": service.update(
            note_id, current_user.id, creds.title, creds.content
        ),
    }


@router.delete("/{note_id}", response_model=UpdatedNotes)
def delete_note(
    note_id: int,
    service: Annotated[NoteService, Depends(get_note_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    return {"success": True, "updated_rows": service.delete(note_id, current_user.id)}
