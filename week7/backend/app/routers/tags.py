from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models import ActionItem, Note, Tag, action_item_tags, note_tags
from backend.app.schemas import (
    ActionItemRead,
    NoteRead,
    TagAssociation,
    TagCreate,
    TagPatch,
    TagRead,
    TagStats,
)

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/stats/summary", response_model=TagStats)
def get_tags_stats(db: Session = Depends(get_db)):
    """Get statistics about tags usage."""
    # Total tags count
    total_count = db.scalar(select(func.count(Tag.id)))

    # Count unique notes that have tags
    notes_tagged = db.scalar(select(func.count(func.distinct(note_tags.c.note_id))))

    # Count unique action items that have tags
    action_items_tagged = db.scalar(
        select(func.count(func.distinct(action_item_tags.c.action_item_id)))
    )

    # Most used tags (top 10)
    # Count usage across both notes and action items
    note_usage = (
        select(note_tags.c.tag_id, func.count(note_tags.c.note_id).label("count"))
        .group_by(note_tags.c.tag_id)
        .subquery()
    )

    action_item_usage = (
        select(
            action_item_tags.c.tag_id, func.count(action_item_tags.c.action_item_id).label("count")
        )
        .group_by(action_item_tags.c.tag_id)
        .subquery()
    )

    # Combine usage counts
    most_used = (
        db.execute(
            select(
                Tag.id,
                Tag.name,
                (
                    func.coalesce(note_usage.c.count, 0)
                    + func.coalesce(action_item_usage.c.count, 0)
                ).label("usage_count"),
            )
            .outerjoin(note_usage, Tag.id == note_usage.c.tag_id)
            .outerjoin(action_item_usage, Tag.id == action_item_usage.c.tag_id)
            .where(
                (func.coalesce(note_usage.c.count, 0) + func.coalesce(action_item_usage.c.count, 0))
                > 0
            )
            .order_by(
                (
                    func.coalesce(note_usage.c.count, 0)
                    + func.coalesce(action_item_usage.c.count, 0)
                ).desc()
            )
            .limit(10)
        )
        .mappings()
        .all()
    )

    most_used_tags = [
        {"id": row["id"], "name": row["name"], "usage_count": row["usage_count"]}
        for row in most_used
    ]

    return TagStats(
        total_count=total_count or 0,
        notes_tagged=notes_tagged or 0,
        action_items_tagged=action_items_tagged or 0,
        most_used_tags=most_used_tags,
    )


@router.get("/", response_model=list[TagRead])
def list_tags(
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    """List all tags with optional search."""
    query = select(Tag)

    if search:
        query = query.where(Tag.name.ilike(f"%{search}%"))

    query = query.offset(skip).limit(limit)
    tags = db.scalars(query).all()

    return tags


@router.get("/{tag_id}", response_model=TagRead)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """Get a single tag by ID."""
    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")
    return tag


@router.post("/", response_model=TagRead, status_code=201)
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    """Create a new tag."""
    # Check if tag with this name already exists
    existing_tag = db.scalar(select(Tag).where(Tag.name == tag.name))
    if existing_tag:
        raise HTTPException(status_code=400, detail=f"Tag with name '{tag.name}' already exists")

    db_tag = Tag(**tag.model_dump())
    db.add(db_tag)
    db.flush()
    db.refresh(db_tag)
    return db_tag


@router.patch("/{tag_id}", response_model=TagRead)
def update_tag(tag_id: int, tag: TagPatch, db: Session = Depends(get_db)):
    """Update a tag."""
    db_tag = db.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    # Check if new name already exists (if name is being changed)
    if tag.name and tag.name != db_tag.name:
        existing_tag = db.scalar(select(Tag).where(Tag.name == tag.name))
        if existing_tag:
            raise HTTPException(
                status_code=400, detail=f"Tag with name '{tag.name}' already exists"
            )

    update_data = tag.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tag, field, value)

    db.flush()
    db.refresh(db_tag)
    return db_tag


@router.delete("/{tag_id}", status_code=204)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    """Delete a tag."""
    db_tag = db.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    db.delete(db_tag)
    db.flush()


# ========== Tag Association Endpoints ==========


@router.post("/notes/{note_id}/tags", response_model=NoteRead, status_code=201)
def associate_tag_with_note(
    note_id: int, tag_association: TagAssociation, db: Session = Depends(get_db)
):
    """Associate one or more tags with a note."""
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")

    for tag_id in tag_association.tag_ids:
        tag = db.get(Tag, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

        if tag not in note.tags:
            note.tags.append(tag)

    db.flush()
    db.refresh(note)
    return note


@router.delete("/notes/{note_id}/tags/{tag_id}", status_code=204)
def disassociate_tag_from_note(note_id: int, tag_id: int, db: Session = Depends(get_db)):
    """Remove a tag association from a note."""
    note = db.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found")

    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    if tag in note.tags:
        note.tags.remove(tag)
        db.flush()


@router.post("/action-items/{item_id}/tags", response_model=ActionItemRead, status_code=201)
def associate_tag_with_action_item(
    item_id: int, tag_association: TagAssociation, db: Session = Depends(get_db)
):
    """Associate one or more tags with an action item."""
    action_item = db.get(ActionItem, item_id)
    if not action_item:
        raise HTTPException(status_code=404, detail=f"Action item with id {item_id} not found")

    for tag_id in tag_association.tag_ids:
        tag = db.get(Tag, tag_id)
        if not tag:
            raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

        if tag not in action_item.tags:
            action_item.tags.append(tag)

    db.flush()
    db.refresh(action_item)
    return action_item


@router.delete("/action-items/{item_id}/tags/{tag_id}", status_code=204)
def disassociate_tag_from_action_item(item_id: int, tag_id: int, db: Session = Depends(get_db)):
    """Remove a tag association from an action item."""
    action_item = db.get(ActionItem, item_id)
    if not action_item:
        raise HTTPException(status_code=404, detail=f"Action item with id {item_id} not found")

    tag = db.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail=f"Tag with id {tag_id} not found")

    if tag in action_item.tags:
        action_item.tags.remove(tag)
        db.flush()
