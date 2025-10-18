from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..db import DatabaseError
from ..schemas import (
    ActionItem,
    ActionItemExtractRequest,
    ActionItemExtractResponse,
    ActionItemStatusUpdate,
)
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post(
    "/extract",
    response_model=ActionItemExtractResponse,
    status_code=status.HTTP_200_OK,
)
def extract(payload: ActionItemExtractRequest) -> ActionItemExtractResponse:
    text = payload.text.strip()
    note_id: Optional[int] = None

    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items(text)
    stored_items = db.insert_action_items(items, note_id=note_id)

    return ActionItemExtractResponse(note_id=note_id, items=stored_items)


@router.post(
    "/extract/llm",
    response_model=ActionItemExtractResponse,
    status_code=status.HTTP_200_OK,
)
def extract_llm(payload: ActionItemExtractRequest) -> ActionItemExtractResponse:
    text = payload.text.strip()
    note_id: Optional[int] = None

    if payload.save_note:
        note_id = db.insert_note(text)

    items = extract_action_items_llm(text, model=payload.model)
    stored_items = db.insert_action_items(items, note_id=note_id)

    return ActionItemExtractResponse(note_id=note_id, items=stored_items)


@router.get("", response_model=List[ActionItem])
def list_all(note_id: Optional[int] = None) -> List[ActionItem]:
    return db.list_action_items(note_id=note_id)


@router.post(
    "/{action_item_id}/done",
    response_model=ActionItem,
    status_code=status.HTTP_200_OK,
)
def mark_done(
    action_item_id: int, payload: ActionItemStatusUpdate
) -> ActionItem:
    try:
        db.mark_action_item_done(action_item_id, payload.done)
    except DatabaseError as exc:
        if "not found" in str(exc).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Action item not found"
            ) from exc
        raise

    updated = db.get_action_item(action_item_id)

    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Action item not found"
        )

    return updated
