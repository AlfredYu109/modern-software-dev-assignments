from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .db import apply_seed_if_needed, engine
from .models import Base
from .routers import action_items as action_items_router
from .routers import notes as notes_router
from .schemas import ErrorDetail, ErrorResponse

app = FastAPI(title="Modern Software Dev Starter (Week 5)")

# Ensure data dir exists
Path("data").mkdir(parents=True, exist_ok=True)

# Mount static frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.on_event("startup")
def startup_event() -> None:
    Base.metadata.create_all(bind=engine)
    apply_seed_if_needed()


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("frontend/index.html")


# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    code = "NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR"
    if exc.status_code == 400:
        code = "BAD_REQUEST"
    elif exc.status_code == 403:
        code = "FORBIDDEN"
    elif exc.status_code == 401:
        code = "UNAUTHORIZED"

    error_response = ErrorResponse(error=ErrorDetail(code=code, message=str(exc.detail)))
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    if errors:
        first_error = errors[0]
        message = f"{first_error['loc'][-1]}: {first_error['msg']}"
    else:
        message = "Validation error"

    error_response = ErrorResponse(error=ErrorDetail(code="VALIDATION_ERROR", message=message))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(),
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    errors = exc.errors()
    if errors:
        first_error = errors[0]
        message = f"{first_error['loc'][-1]}: {first_error['msg']}"
    else:
        message = "Validation error"

    error_response = ErrorResponse(error=ErrorDetail(code="VALIDATION_ERROR", message=message))
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(),
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    error_response = ErrorResponse(
        error=ErrorDetail(code="DATABASE_ERROR", message="A database error occurred")
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    error_response = ErrorResponse(
        error=ErrorDetail(code="INTERNAL_ERROR", message="An internal error occurred")
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(),
    )


# Routers
app.include_router(notes_router.router)
app.include_router(action_items_router.router)
