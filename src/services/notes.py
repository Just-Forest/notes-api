from collections.abc import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from src.database.note import Note
from src.services.exceptions import NotFound


class NoteService:
    def __init__(self, session: Session):
        self.session = session

    def list_for_user(self, user_id: int) -> Sequence[Note]:
        stmt = select(Note).where(Note.user_id == user_id)
        return self.session.execute(stmt).scalars().all()

    def create(self, user_id: int, title: str, content: str) -> Note:
        note = Note(title=title, content=content, user_id=user_id)
        self.session.add(note)
        self.session.commit()
        self.session.refresh(note)
        return note

    def update(self, note_id: int, user_id: int, title: str, content: str) -> None:
        stmt = (
            update(Note)
            .where(Note.id == note_id, Note.user_id == user_id)
            .values(title=title, content=content)
        )
        if self.session.execute(stmt).rowcount == 0:
            raise NotFound("Note not found")
        self.session.commit()

    def delete(self, note_id: int, user_id: int) -> None:
        stmt = delete(Note).where(Note.id == note_id, Note.user_id == user_id)
        if self.session.execute(stmt).rowcount == 0:
            raise NotFound("Note not found")
        self.session.commit()