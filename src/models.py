from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str  # "todo" | "in_progress" | "done"
    created_at: str  # ISO string


def get_db_path() -> str:
    # Banco local simples (p/ trabalho acadêmico)
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir / "app.db")


def connect(db_path: Optional[str] = None) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path or get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            status TEXT NOT NULL DEFAULT 'todo',
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_task(conn: sqlite3.Connection, title: str, description: str = "") -> Task:
    title = (title or "").strip()
    description = (description or "").strip()

    if len(title) < 3:
        raise ValueError("title must have at least 3 characters")

    cur = conn.execute(
        "INSERT INTO tasks(title, description, status, created_at) VALUES (?, ?, 'todo', ?)",
        (title, description, now_iso()),
    )
    conn.commit()
    return get_task(conn, int(cur.lastrowid))


def get_task(conn: sqlite3.Connection, task_id: int) -> Task:
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise KeyError("task not found")
    return Task(**dict(row))


def list_tasks(conn: sqlite3.Connection, status: Optional[str] = None) -> list[Task]:
    if status:
        rows = conn.execute("SELECT * FROM tasks WHERE status = ? ORDER BY id DESC", (status,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return [Task(**dict(r)) for r in rows]


def update_task(
    conn: sqlite3.Connection,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> Task:
    # Validações mínimas
    if status is not None and status not in {"todo", "in_progress", "done"}:
        raise ValueError("invalid status")

    # Garante existência
    _ = get_task(conn, task_id)

    fields = []
    values = []

    if title is not None:
        title = title.strip()
        if len(title) < 3:
            raise ValueError("title must have at least 3 characters")
        fields.append("title = ?")
        values.append(title)

    if description is not None:
        fields.append("description = ?")
        values.append(description.strip())

    if status is not None:
        fields.append("status = ?")
        values.append(status)

    if not fields:
        return get_task(conn, task_id)

    values.append(task_id)
    conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()
    return get_task(conn, task_id)


def delete_task(conn: sqlite3.Connection, task_id: int) -> None:
    # Garante existência
    _ = get_task(conn, task_id)
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
