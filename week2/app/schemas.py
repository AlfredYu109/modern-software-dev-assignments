from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, constr


class NoteCreate(BaseModel):
    content: constr(strip_whitespace=True, min_length=1)  # type: ignore[type-arg]


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str

    class Config:
        orm_mode = True


class ActionItem(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: Optional[str] = None

    class Config:
        orm_mode = True


class ActionItemExtractRequest(BaseModel):
    text: constr(strip_whitespace=True, min_length=1)  # type: ignore[type-arg]
    save_note: bool = False
    model: Optional[str] = None


class ActionItemExtractResponse(BaseModel):
    note_id: Optional[int]
    items: List[ActionItem]


class ActionItemStatusUpdate(BaseModel):
    done: bool = True
