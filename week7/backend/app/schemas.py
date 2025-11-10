from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Note title")
    content: str = Field(..., min_length=1, description="Note content")

    @field_validator("title", "content")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip()


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200, description="Note title")
    content: str | None = Field(None, min_length=1, description="Note content")

    @field_validator("title", "content")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Field cannot be empty or whitespace only")
        return v.strip() if v else None


class ActionItemCreate(BaseModel):
    description: str = Field(
        ..., min_length=1, max_length=500, description="Action item description"
    )

    @field_validator("description")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Description cannot be empty or whitespace only")
        return v.strip()


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = Field(
        None, min_length=1, max_length=500, description="Action item description"
    )
    completed: bool | None = None

    @field_validator("description")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Description cannot be empty or whitespace only")
        return v.strip() if v else None


class BulkCreateNotes(BaseModel):
    notes: list[NoteCreate] = Field(
        ..., min_length=1, max_length=100, description="List of notes to create"
    )


class BulkCreateActionItems(BaseModel):
    items: list[ActionItemCreate] = Field(
        ..., min_length=1, max_length=100, description="List of action items to create"
    )


class BulkDeleteRequest(BaseModel):
    ids: list[int] = Field(..., min_length=1, max_length=100, description="List of IDs to delete")


class BulkCompleteRequest(BaseModel):
    ids: list[int] = Field(
        ..., min_length=1, max_length=100, description="List of action item IDs to mark as complete"
    )


class NotesStats(BaseModel):
    total_count: int
    total_characters: int
    average_content_length: float


class ActionItemsStats(BaseModel):
    total_count: int
    completed_count: int
    pending_count: int
    completion_rate: float
