from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=2000)

    @field_validator("title", "content", mode="before")
    @classmethod
    def strip_text(cls, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
        return value


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = Field(default=None, min_length=1, max_length=2000)

    @field_validator("title", "content", mode="before")
    @classmethod
    def strip_optional_text(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, str):
            value = value.strip()
        return value

    @model_validator(mode="after")
    def ensure_payload_present(self) -> "NotePatch":
        if self.title is None and self.content is None:
            raise ValueError("At least one field must be provided")
        return self


class ActionItemCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)

    @field_validator("description", mode="before")
    @classmethod
    def strip_description(cls, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
        return value


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: Optional[str] = Field(default=None, min_length=1, max_length=500)
    completed: Optional[bool] = None

    @field_validator("description", mode="before")
    @classmethod
    def strip_optional_description(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, str):
            value = value.strip()
        return value

    @model_validator(mode="after")
    def ensure_patch_fields_present(self) -> "ActionItemPatch":
        if self.description is None and self.completed is None:
            raise ValueError("At least one field must be provided")
        return self
