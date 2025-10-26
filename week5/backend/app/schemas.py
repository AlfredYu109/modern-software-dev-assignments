from typing import Generic, TypeVar

from pydantic import BaseModel, Field, field_validator


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)

    @field_validator("title", "content")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v


class NoteRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    description: str = Field(..., min_length=1)

    @field_validator("description")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Description cannot be empty or whitespace only")
        return v


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool

    class Config:
        from_attributes = True


# Response envelope models
T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    ok: bool = False
    error: ErrorDetail


class SuccessResponse(BaseModel, Generic[T]):
    ok: bool = True
    data: T
