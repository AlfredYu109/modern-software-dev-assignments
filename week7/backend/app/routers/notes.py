from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import (
    BulkCreateNotes,
    BulkDeleteRequest,
    NoteCreate,
    NotePatch,
    NoteRead,
    NotesStats,
)

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> list[NoteRead]:
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(Note, sort_field):
        stmt = stmt.order_by(order_fn(getattr(Note, sort_field)))
    else:
        stmt = stmt.order_by(desc(Note.created_at))

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
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
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
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteRead.model_validate(note)


@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db)) -> None:
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with ID {note_id} not found")
    db.delete(note)
    db.flush()


@router.post("/bulk", response_model=list[NoteRead], status_code=201)
def bulk_create_notes(payload: BulkCreateNotes, db: Session = Depends(get_db)) -> list[NoteRead]:
    if not payload.notes:
        raise HTTPException(status_code=400, detail="No notes provided for bulk creation")

    notes = [Note(title=note.title, content=note.content) for note in payload.notes]
    db.add_all(notes)
    db.flush()
    for note in notes:
        db.refresh(note)
    return [NoteRead.model_validate(note) for note in notes]


@router.post("/bulk/delete", status_code=200)
def bulk_delete_notes(payload: BulkDeleteRequest, db: Session = Depends(get_db)) -> dict[str, int]:
    if not payload.ids:
        raise HTTPException(status_code=400, detail="No IDs provided for bulk deletion")

    stmt = select(Note).where(Note.id.in_(payload.ids))
    notes = db.execute(stmt).scalars().all()

    if len(notes) != len(payload.ids):
        found_ids = {note.id for note in notes}
        missing_ids = set(payload.ids) - found_ids
        raise HTTPException(
            status_code=404,
            detail=f"Some notes not found. Missing IDs: {sorted(missing_ids)}",
        )

    for note in notes:
        db.delete(note)
    db.flush()

    return {"deleted_count": len(notes)}


@router.get("/stats/summary", response_model=NotesStats)
def get_notes_stats(db: Session = Depends(get_db)) -> NotesStats:
    stmt = select(
        func.count(Note.id).label("total_count"),
        func.sum(func.length(Note.content)).label("total_characters"),
        func.avg(func.length(Note.content)).label("average_content_length"),
    )
    result = db.execute(stmt).one()

    return NotesStats(
        total_count=result.total_count or 0,
        total_characters=result.total_characters or 0,
        average_content_length=float(result.average_content_length or 0),
    )
