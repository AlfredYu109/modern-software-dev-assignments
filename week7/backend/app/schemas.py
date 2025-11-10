from __future__ import annotations

# ruff: noqa: UP006,UP007  # maintain Optional usage for Python 3.7 compatibility
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
    def ensure_payload_present(self) -> NotePatch:
        if self.title is None and self.content is None:
            raise ValueError("At least one field must be provided")
        return self


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("name", "description", mode="before")
    @classmethod
    def strip_project_text(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, str):
            value = value.strip()
        return value


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=2000)

    @field_validator("name", "description", mode="before")
    @classmethod
    def strip_optional(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, str):
            value = value.strip()
        return value

    @model_validator(mode="after")
    def ensure_patch_values(self) -> ProjectUpdate:
        if self.name is None and self.description is None:
            raise ValueError("At least one field must be provided")
        return self


class ProjectRead(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectSummary(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    project_id: Optional[int] = None

    @field_validator("description", mode="before")
    @classmethod
    def strip_description(cls, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
        return value

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value < 1:
            raise ValueError("project_id must be positive")
        return value


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    project_id: Optional[int] = None
    project: Optional[ProjectSummary] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: Optional[str] = Field(default=None, min_length=1, max_length=500)
    completed: Optional[bool] = None
    project_id: Optional[int] = None

    @field_validator("description", mode="before")
    @classmethod
    def strip_optional_description(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, str):
            value = value.strip()
        return value

    @field_validator("project_id")
    @classmethod
    def validate_optional_project_id(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value < 1:
            raise ValueError("project_id must be positive")
        return value

    @model_validator(mode="after")
    def ensure_patch_fields_present(self) -> ActionItemPatch:
        if (
            self.description is None
            and self.completed is None
            and "project_id" not in self.model_fields_set
        ):
            raise ValueError("At least one field must be provided")
        return self
