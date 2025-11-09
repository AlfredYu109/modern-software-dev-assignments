from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NoteRead, SuccessResponse

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=SuccessResponse[list[NoteRead]])
def list_notes(db: Session = Depends(get_db)) -> SuccessResponse[list[NoteRead]]:
    rows = db.execute(select(Note)).scalars().all()
    notes = [NoteRead.model_validate(row) for row in rows]
    return SuccessResponse(data=notes)


@router.post("/", response_model=SuccessResponse[NoteRead], status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> SuccessResponse[NoteRead]:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return SuccessResponse(data=NoteRead.model_validate(note))


@router.get("/search/", response_model=SuccessResponse[list[NoteRead]])
def search_notes(
    q: Optional[str] = None, db: Session = Depends(get_db)
) -> SuccessResponse[list[NoteRead]]:
    if not q:
        rows = db.execute(select(Note)).scalars().all()
    else:
        rows = (
            db.execute(select(Note).where((Note.title.contains(q)) | (Note.content.contains(q))))
            .scalars()
            .all()
        )
    notes = [NoteRead.model_validate(row) for row in rows]
    return SuccessResponse(data=notes)


@router.get("/{note_id}", response_model=SuccessResponse[NoteRead])
def get_note(note_id: int, db: Session = Depends(get_db)) -> SuccessResponse[NoteRead]:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return SuccessResponse(data=NoteRead.model_validate(note))
