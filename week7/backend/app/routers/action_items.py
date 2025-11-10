from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, func, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import (
    ActionItemCreate,
    ActionItemPatch,
    ActionItemRead,
    ActionItemsStats,
    BulkCompleteRequest,
    BulkCreateActionItems,
    BulkDeleteRequest,
)

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=list[ActionItemRead])
def list_items(
    db: Session = Depends(get_db),
    completed: Optional[bool] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at"),
) -> list[ActionItemRead]:
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    if hasattr(ActionItem, sort_field):
        stmt = stmt.order_by(order_fn(getattr(ActionItem, sort_field)))
    else:
        stmt = stmt.order_by(desc(ActionItem.created_at))

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    item = ActionItem(description=payload.description, completed=False, note_id=payload.note_id)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.post("/bulk", response_model=list[ActionItemRead], status_code=201)
def bulk_create_items(
    payload: BulkCreateActionItems, db: Session = Depends(get_db)
) -> list[ActionItemRead]:
    if not payload.items:
        raise HTTPException(status_code=400, detail="No action items provided for bulk creation")

    items = [
        ActionItem(description=item.description, completed=False, note_id=item.note_id)
        for item in payload.items
    ]
    db.add_all(items)
    db.flush()
    for item in items:
        db.refresh(item)
    return [ActionItemRead.model_validate(item) for item in items]


@router.post("/bulk/delete", status_code=200)
def bulk_delete_items(payload: BulkDeleteRequest, db: Session = Depends(get_db)) -> dict[str, int]:
    if not payload.ids:
        raise HTTPException(status_code=400, detail="No IDs provided for bulk deletion")

    stmt = select(ActionItem).where(ActionItem.id.in_(payload.ids))
    items = db.execute(stmt).scalars().all()

    if len(items) != len(payload.ids):
        found_ids = {item.id for item in items}
        missing_ids = set(payload.ids) - found_ids
        raise HTTPException(
            status_code=404,
            detail=f"Some action items not found. Missing IDs: {sorted(missing_ids)}",
        )

    for item in items:
        db.delete(item)
    db.flush()

    return {"deleted_count": len(items)}


@router.put("/bulk/complete", response_model=list[ActionItemRead])
def bulk_complete_items(
    payload: BulkCompleteRequest, db: Session = Depends(get_db)
) -> list[ActionItemRead]:
    if not payload.ids:
        raise HTTPException(status_code=400, detail="No IDs provided for bulk completion")

    stmt = select(ActionItem).where(ActionItem.id.in_(payload.ids))
    items = db.execute(stmt).scalars().all()

    if len(items) != len(payload.ids):
        found_ids = {item.id for item in items}
        missing_ids = set(payload.ids) - found_ids
        raise HTTPException(
            status_code=404,
            detail=f"Some action items not found. Missing IDs: {sorted(missing_ids)}",
        )

    for item in items:
        item.completed = True
        db.add(item)

    db.flush()
    for item in items:
        db.refresh(item)

    return [ActionItemRead.model_validate(item) for item in items]


@router.get("/stats/summary", response_model=ActionItemsStats)
def get_action_items_stats(db: Session = Depends(get_db)) -> ActionItemsStats:
    total_stmt = select(func.count(ActionItem.id))
    total_count = db.execute(total_stmt).scalar() or 0

    completed_stmt = select(func.count(ActionItem.id)).where(ActionItem.completed.is_(True))
    completed_count = db.execute(completed_stmt).scalar() or 0

    pending_count = total_count - completed_count
    completion_rate = (completed_count / total_count * 100) if total_count > 0 else 0.0

    return ActionItemsStats(
        total_count=total_count,
        completed_count=completed_count,
        pending_count=pending_count,
        completion_rate=round(completion_rate, 2),
    )


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.patch("/{item_id}", response_model=ActionItemRead)
def patch_item(
    item_id: int, payload: ActionItemPatch, db: Session = Depends(get_db)
) -> ActionItemRead:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    if payload.description is not None:
        item.description = payload.description
    if payload.completed is not None:
        item.completed = payload.completed
    if payload.note_id is not None:
        item.note_id = payload.note_id
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Action item with ID {item_id} not found")
    db.delete(item)
    db.flush()
