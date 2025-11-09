from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem
from ..schemas import ActionItemCreate, ActionItemRead, SuccessResponse

router = APIRouter(prefix="/action-items", tags=["action_items"])


@router.get("/", response_model=SuccessResponse[list[ActionItemRead]])
def list_items(db: Session = Depends(get_db)) -> SuccessResponse[list[ActionItemRead]]:
    rows = db.execute(select(ActionItem)).scalars().all()
    items = [ActionItemRead.model_validate(row) for row in rows]
    return SuccessResponse(data=items)


@router.post("/", response_model=SuccessResponse[ActionItemRead], status_code=201)
def create_item(
    payload: ActionItemCreate, db: Session = Depends(get_db)
) -> SuccessResponse[ActionItemRead]:
    item = ActionItem(description=payload.description, completed=False)
    db.add(item)
    db.flush()
    db.refresh(item)
    return SuccessResponse(data=ActionItemRead.model_validate(item))


@router.put("/{item_id}/complete", response_model=SuccessResponse[ActionItemRead])
def complete_item(item_id: int, db: Session = Depends(get_db)) -> SuccessResponse[ActionItemRead]:
    item = db.get(ActionItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    item.completed = True
    db.add(item)
    db.flush()
    db.refresh(item)
    return SuccessResponse(data=ActionItemRead.model_validate(item))
