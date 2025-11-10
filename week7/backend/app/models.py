from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


# Association table for Note <-> Tag many-to-many relationship
note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


# Association table for ActionItem <-> Tag many-to-many relationship
action_item_tags = Table(
    "action_item_tags",
    Base.metadata,
    Column(
        "action_item_id",
        Integer,
        ForeignKey("action_items.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base, TimestampMixin):
    """Tag model for categorizing notes and action items."""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True, index=True)
    color = Column(String(7), nullable=True)  # Hex color code (e.g., #FF5733)

    # Relationships
    notes = relationship("Note", secondary=note_tags, back_populates="tags")
    action_items = relationship("ActionItem", secondary=action_item_tags, back_populates="tags")


class Note(Base, TimestampMixin):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)

    # Relationships
    action_items = relationship(
        "ActionItem",
        back_populates="note",
        cascade="all, delete-orphan",
        foreign_keys="ActionItem.note_id",
    )
    tags = relationship("Tag", secondary=note_tags, back_populates="notes")


class ActionItem(Base, TimestampMixin):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=True, index=True)

    # Relationships
    note = relationship("Note", back_populates="action_items", foreign_keys=[note_id])
    tags = relationship("Tag", secondary=action_item_tags, back_populates="action_items")
