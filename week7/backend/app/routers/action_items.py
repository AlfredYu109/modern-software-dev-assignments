from __future__ import annotations

# ruff: noqa: UP006,UP007  # keep typing.List/Optional for Python 3.7 compatibility at runtime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Project
from ..schemas import ActionItemCreate, ActionItemPatch, ActionItemRead

router = APIRouter(prefix="/action-items", tags=["action_items"])
ALLOWED_SORT_FIELDS = {
    "created_at": ActionItem.created_at,
    "updated_at": ActionItem.updated_at,
    "description": ActionItem.description,
    "id": ActionItem.id,
    "project_id": ActionItem.project_id,
}


def _apply_sorting(sort_param: str, stmt):
    sort_field = sort_param.lstrip("-")
    column = ALLOWED_SORT_FIELDS.get(sort_field)
    if column is None:
        raise HTTPException(status_code=400, detail=f"Unsupported sort field '{sort_field}'")
    order_fn = desc if sort_param.startswith("-") else asc
    return stmt.order_by(order_fn(column))


def _get_item_or_404(db: Session, item_id: int) -> ActionItem:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return item


@router.get("/", response_model=List[ActionItemRead])
def list_items(
    db: Session = Depends(get_db),
    completed: Optional[bool] = None,
    project_id: Optional[int] = Query(default=None, ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    sort: str = Query("-created_at"),
) -> List[ActionItemRead]:
    stmt = select(ActionItem)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))
    if project_id is not None:
        stmt = stmt.where(ActionItem.project_id == project_id)

    stmt = _apply_sorting(sort, stmt)

    rows = db.execute(stmt.offset(skip).limit(limit)).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]


@router.post("/", response_model=ActionItemRead, status_code=201)
def create_item(payload: ActionItemCreate, db: Session = Depends(get_db)) -> ActionItemRead:
    project = None
    if payload.project_id is not None:
        project = db.get(Project, payload.project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
    item = ActionItem(description=payload.description, completed=False, project=project)
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.put("/{item_id}/complete", response_model=ActionItemRead)
def complete_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = _get_item_or_404(db, item_id)
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.get("/{item_id}", response_model=ActionItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> ActionItemRead:
    item = _get_item_or_404(db, item_id)
    return ActionItemRead.model_validate(item)


@router.patch("/{item_id}", response_model=ActionItemRead)
def patch_item(
    item_id: int, payload: ActionItemPatch, db: Session = Depends(get_db)
) -> ActionItemRead:
    item = _get_item_or_404(db, item_id)
    if payload.description is not None:
        item.description = payload.description
    if payload.completed is not None:
        item.completed = payload.completed
    if "project_id" in payload.model_fields_set:
        if payload.project_id is None:
            item.project = None
        else:
            project = db.get(Project, payload.project_id)
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            item.project = project
    db.add(item)
    db.flush()
    db.refresh(item)
    return ActionItemRead.model_validate(item)


@router.delete("/{item_id}", status_code=204, response_class=Response)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Response:
    item = _get_item_or_404(db, item_id)
    db.delete(item)
    db.flush()
    return Response(status_code=204)
