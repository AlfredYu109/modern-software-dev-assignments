from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional

from .config import get_settings


class DatabaseError(RuntimeError):
    """Raised when a database operation fails."""


def _get_db_path() -> Path:
    settings = get_settings()
    db_path = settings.database_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path


def _connect() -> sqlite3.Connection:
    db_path = _get_db_path()
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    connection = _connect()
    try:
        yield connection
    except sqlite3.Error as exc:
        raise DatabaseError("Database operation failed") from exc
    finally:
        connection.close()


def init_db() -> None:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );
            """
        )
        connection.commit()


def insert_note(content: str) -> int:
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
            connection.commit()
            return int(cursor.lastrowid)
    except sqlite3.Error as exc:  # pragma: no cover - defensive
        raise DatabaseError("Failed to insert note") from exc


def list_notes() -> List[Dict[str, Any]]:
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes ORDER BY id DESC"
            )
            rows = cursor.fetchall()
            return [_row_to_note(row) for row in rows]
    except sqlite3.Error as exc:  # pragma: no cover - defensive
        raise DatabaseError("Failed to list notes") from exc


def get_note(note_id: int) -> Optional[Dict[str, Any]]:
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, content, created_at FROM notes WHERE id = ?",
                (note_id,),
            )
            row = cursor.fetchone()
            return _row_to_note(row) if row else None
    except sqlite3.Error as exc:  # pragma: no cover - defensive
        raise DatabaseError("Failed to fetch note") from exc


def insert_action_items(
    items: List[str], note_id: Optional[int] = None
) -> List[Dict[str, Any]]:
    if not items:
        return []
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            created: List[Dict[str, Any]] = []
            for item in items:
                cursor.execute(
                    "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                    (note_id, item),
                )
                item_id = int(cursor.lastrowid)
                created.append(_fetch_action_item(cursor, item_id))
            connection.commit()
            return created
    except sqlite3.Error as exc:  # pragma: no cover - defensive
        raise DatabaseError("Failed to insert action items") from exc


def list_action_items(note_id: Optional[int] = None) -> List[Dict[str, Any]]:
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            if note_id is None:
                cursor.execute(
                    """
                    SELECT id, note_id, text, done, created_at
                    FROM action_items
                    ORDER BY id DESC
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT id, note_id, text, done, created_at
                    FROM action_items
                    WHERE note_id = ?
                    ORDER BY id DESC
                    """,
                    (note_id,),
                )
            rows = cursor.fetchall()
            return [_row_to_action_item(row) for row in rows]
    except sqlite3.Error as exc:  # pragma: no cover - defensive
        raise DatabaseError("Failed to list action items") from exc


def mark_action_item_done(action_item_id: int, done: bool) -> None:
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE action_items SET done = ? WHERE id = ?",
                (1 if done else 0, action_item_id),
            )
            if cursor.rowcount == 0:
                raise DatabaseError("Action item not found")
            connection.commit()
    except sqlite3.Error as exc:  # pragma: no cover - defensive
        raise DatabaseError("Failed to update action item status") from exc
    except DatabaseError:
        raise


def get_action_item(action_item_id: int) -> Optional[Dict[str, Any]]:
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, note_id, text, done, created_at
                FROM action_items
                WHERE id = ?
                """,
                (action_item_id,),
            )
            row = cursor.fetchone()
            return _row_to_action_item(row) if row else None
    except sqlite3.Error as exc:  # pragma: no cover - defensive
        raise DatabaseError("Failed to fetch action item") from exc


def _fetch_action_item(cursor: sqlite3.Cursor, item_id: int) -> Dict[str, Any]:
    cursor.execute(
        """
        SELECT id, note_id, text, done, created_at
        FROM action_items
        WHERE id = ?
        """,
        (item_id,),
    )
    row = cursor.fetchone()
    if row is None:  # pragma: no cover - defensive
        raise DatabaseError("Inserted action item could not be retrieved")
    return _row_to_action_item(row)


def _row_to_note(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": int(row["id"]),
        "content": str(row["content"]),
        "created_at": row["created_at"],
    }


def _row_to_action_item(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": int(row["id"]),
        "note_id": int(row["note_id"]) if row["note_id"] is not None else None,
        "text": str(row["text"]),
        "done": bool(row["done"]),
        "created_at": row["created_at"],
    }
