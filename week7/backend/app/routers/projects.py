from __future__ import annotations

# ruff: noqa: UP006,UP007  # keep typing.List/Optional for Python 3.7 compatibility at runtime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import ActionItem, Project
from ..schemas import (
    ActionItemRead,
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
)

router = APIRouter(prefix="/projects", tags=["projects"])


def _get_project_or_404(db: Session, project_id: int) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/", response_model=List[ProjectRead])
def list_projects(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
) -> List[ProjectRead]:
    stmt = select(Project).offset(skip).limit(limit).order_by(Project.created_at.desc())
    rows = db.execute(stmt).scalars().all()
    return [ProjectRead.model_validate(row) for row in rows]


@router.post("/", response_model=ProjectRead, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    db.flush()
    db.refresh(project)
    return ProjectRead.model_validate(project)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    project = _get_project_or_404(db, project_id)
    return ProjectRead.model_validate(project)


@router.patch("/{project_id}", response_model=ProjectRead)
def patch_project(
    project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)
) -> ProjectRead:
    project = _get_project_or_404(db, project_id)
    if payload.name is not None:
        project.name = payload.name
    if payload.description is not None:
        project.description = payload.description
    db.add(project)
    db.flush()
    db.refresh(project)
    return ProjectRead.model_validate(project)


@router.delete("/{project_id}", status_code=204, response_class=Response)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> Response:
    project = _get_project_or_404(db, project_id)
    items = db.execute(select(ActionItem).where(ActionItem.project_id == project_id)).scalars()
    for item in items:
        item.project = None
        db.add(item)
    db.delete(project)
    db.flush()
    return Response(status_code=204)


@router.get("/{project_id}/action-items", response_model=List[ActionItemRead])
def list_project_action_items(
    project_id: int,
    db: Session = Depends(get_db),
    completed: Optional[bool] = None,
) -> List[ActionItemRead]:
    _get_project_or_404(db, project_id)
    stmt = select(ActionItem).where(ActionItem.project_id == project_id)
    if completed is not None:
        stmt = stmt.where(ActionItem.completed.is_(completed))
    rows = db.execute(stmt.order_by(ActionItem.created_at.desc())).scalars().all()
    return [ActionItemRead.model_validate(row) for row in rows]
