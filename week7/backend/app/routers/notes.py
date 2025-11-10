from __future__ import annotations

# ruff: noqa: UP006,UP007  # keep typing.List/Optional for Python 3.7 compatibility at runtime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NotePatch, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])
ALLOWED_SORT_FIELDS = {
    "created_at": Note.created_at,
    "updated_at": Note.updated_at,
    "title": Note.title,
    "id": Note.id,
}


def _apply_sorting(sort_param: str, stmt):
    sort_field = sort_param.lstrip("-")
    column = ALLOWED_SORT_FIELDS.get(sort_field)
    if column is None:
        raise HTTPException(status_code=400, detail=f"Unsupported sort field '{sort_field}'")
    order_fn = desc if sort_param.startswith("-") else asc
    return stmt.order_by(order_fn(column))


def _get_note_or_404(db: Session, note_id: int) -> Note:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> List[NoteRead]:
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    stmt = _apply_sorting(sort, stmt)

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.post("/", response_model=NoteRead, status_code=201)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteRead:
    note = Note(title=payload.title, content=payload.content)
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.patch("/{note_id}", response_model=NoteRead)
def patch_note(note_id: int, payload: NotePatch, db: Session = Depends(get_db)) -> NoteRead:
    note = _get_note_or_404(db, note_id)
    if payload.title is not None:
        note.title = payload.title
    if payload.content is not None:
        note.content = payload.content
    db.add(note)
    db.flush()
    db.refresh(note)
    return NoteRead.model_validate(note)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)) -> NoteRead:
    note = _get_note_or_404(db, note_id)
    return NoteRead.model_validate(note)


@router.delete("/{note_id}", status_code=204, response_class=Response)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> Response:
    note = _get_note_or_404(db, note_id)
    db.delete(note)
    db.flush()
    return Response(status_code=204)
