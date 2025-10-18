from __future__ import annotations

from typing import List

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..schemas import NoteCreate, NoteResponse


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate) -> NoteResponse:
    note_id = db.insert_note(payload.content.strip())
    note = db.get_note(note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Note could not be created",
        )
    return note


@router.get("/{note_id}", response_model=NoteResponse)
def get_single_note(note_id: int) -> NoteResponse:
    note = db.get_note(note_id)

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="note not found")

    return note


@router.get("", response_model=List[NoteResponse])
def list_notes() -> List[NoteResponse]:
    return db.list_notes()
