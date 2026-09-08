import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

from config import DB_PATH

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    """Crée la table si elle n'existe pas encore"""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memory (
                user_id    TEXT NOT NULL,
                key        TEXT NOT NULL,
                value      TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (user_id, key)
            )
            """
        )

def remember(user_id: str, key: str, value: str) -> str:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO memory (user_id, key, value, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id, key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at
            """,
            (user_id, key, value, datetime.now(timezone.utc).isoformat()),
        )
    return f"Mémorisé : {key} = {value}"

def recall(user_id: str, key: str) -> str:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT value FROM memory WHERE user_id = ? AND key = ?",
            (user_id, key),
        ).fetchone()
    return row["value"] if row else f"Aucune information mémorisée pour '{key}'."

def recall_all(user_id: str) -> dict:
    """Utile pour du débogage ou pour injecter tout le contexte connu d'un utilisateur."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT key, value FROM memory WHERE user_id = ?", (user_id,)
        ).fetchall()
    return {row["key"]: row["value"] for row in rows}