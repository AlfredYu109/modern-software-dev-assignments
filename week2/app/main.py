from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .db import DatabaseError, init_db
from .routers import action_items, notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Action Item Extractor", lifespan=lifespan)


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    html_path = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    return html_path.read_text(encoding="utf-8")


app.include_router(notes.router)
app.include_router(action_items.router)


static_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.exception_handler(DatabaseError)
async def handle_database_error(request: Request, exc: DatabaseError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )
