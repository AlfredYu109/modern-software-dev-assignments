from datetime import datetime

from pydantic import BaseModel, Field, field_validator


# ========== Tag Schemas ==========
class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Tag name")
    color: str | None = Field(
        None, pattern=r"^#[0-9A-Fa-f]{6}$", description="Hex color code (e.g., #FF5733)"
    )

    @field_validator("name")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Tag name cannot be empty or whitespace only")
        return v.strip()


class TagRead(BaseModel):
    id: int
    name: str
    color: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TagPatch(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=50, description="Tag name")
    color: str | None = Field(
        None, pattern=r"^#[0-9A-Fa-f]{6}$", description="Hex color code (e.g., #FF5733)"
    )

    @field_validator("name")
    @classmethod
    def validate_not_empty(cls, v: str | None) -> str | None:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Tag name cannot be empty or whitespace only")
        return v.strip() if v else None


class TagAssociation(BaseModel):
    tag_ids: list[int] = Field(..., min_length=1, max_length=50, description="List of tag IDs")


# ========== Note Schemas ==========
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
    tags: list["TagRead"] = []

    class Config:
        from_attributes = True


class NoteReadWithActionItems(BaseModel):
    """Note response with nested action items."""

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    tags: list["TagRead"] = []
    action_items: list["ActionItemRead"] = []

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
    note_id: int | None = Field(None, description="Optional note ID to associate with")

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
    note_id: int | None
    created_at: datetime
    updated_at: datetime
    tags: list["TagRead"] = []

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = Field(
        None, min_length=1, max_length=500, description="Action item description"
    )
    completed: bool | None = None
    note_id: int | None = Field(None, description="Optional note ID to associate with")

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


class TagStats(BaseModel):
    total_count: int
    notes_tagged: int
    action_items_tagged: int
    most_used_tags: list[dict[str, int | str]]  # List of {id, name, usage_count}
