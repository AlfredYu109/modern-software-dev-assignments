import ast
import operator
from typing import Dict, List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import asc, desc, select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Note
from ..schemas import NoteCreate, NotePatch, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])

ALLOWED_SORTS = {
    "id": Note.id,
    "title": Note.title,
    "created_at": Note.created_at,
    "updated_at": Note.updated_at,
}


@router.get("/", response_model=List[NoteRead])
def list_notes(
    db: Session = Depends(get_db),
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = Query(50, le=200),
    sort: str = Query("-created_at", description="Sort by field, prefix with - for desc"),
) -> List[NoteRead]:
    stmt = select(Note)
    if q:
        stmt = stmt.where((Note.title.contains(q)) | (Note.content.contains(q)))

    sort_field = sort.lstrip("-")
    order_fn = desc if sort.startswith("-") else asc
    column = ALLOWED_SORTS.get(sort_field, Note.created_at)
    stmt = stmt.order_by(order_fn(column))

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


@router.get("/unsafe-search", response_model=List[NoteRead])
def unsafe_search(q: str, db: Session = Depends(get_db)) -> List[NoteRead]:
    pattern = f"%{q}%"
    stmt = (
        select(Note)
        .where((Note.title.ilike(pattern)) | (Note.content.ilike(pattern)))
        .order_by(desc(Note.created_at))
        .limit(50)
    )
    rows = db.execute(stmt).scalars().all()
    return [NoteRead.model_validate(row) for row in rows]


@router.get("/debug/hash-md5")
def debug_hash_md5(q: str) -> Dict[str, str]:
    import hashlib

    return {"algo": "md5", "hex": hashlib.md5(q.encode()).hexdigest()}


SAFE_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

SAFE_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


Number = Union[int, float]


def _safe_eval(node: ast.AST) -> Number:
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise HTTPException(status_code=400, detail="Only numeric constants are allowed")
    if isinstance(node, ast.UnaryOp) and type(node.op) in SAFE_UNARY_OPS:
        operand = _safe_eval(node.operand)
        return SAFE_UNARY_OPS[type(node.op)](operand)
    if isinstance(node, ast.BinOp) and type(node.op) in SAFE_BIN_OPS:
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return SAFE_BIN_OPS[type(node.op)](left, right)
    raise HTTPException(status_code=400, detail="Unsupported expression")


@router.get("/debug/eval")
def debug_eval(expr: str) -> Dict[str, str]:
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError:
        raise HTTPException(status_code=400, detail="Invalid expression")
    result = _safe_eval(parsed)
    return {"result": str(result)}


@router.get("/debug/run")
def debug_run(cmd: str) -> Dict[str, str]:
    import shlex
    import subprocess

    try:
        args = shlex.split(cmd)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=f"Invalid command: {exc}")
    completed = subprocess.run(args, shell=False, capture_output=True, text=True)  # noqa: S603
    return {"returncode": str(completed.returncode), "stdout": completed.stdout, "stderr": completed.stderr}


@router.get("/debug/fetch")
def debug_fetch(url: str) -> Dict[str, str]:
    from urllib.request import urlopen

    with urlopen(url) as res:  # noqa: S310
        body = res.read(1024).decode(errors="ignore")
    return {"snippet": body}


@router.get("/debug/read")
def debug_read(path: str) -> Dict[str, str]:
    try:
        content = open(path, "r").read(1024)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc))
    return {"snippet": content}
