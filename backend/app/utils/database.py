"""SQLite-based lightweight persistence layer for StadiumGPT."""

from __future__ import annotations

import json
import logging
import os
import sqlite3
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Database:
    """Thin async wrapper over SQLite (sufficient for demo/challenge scope)."""

    def __init__(self) -> None:
        self.db_path = os.path.join(os.path.dirname(__file__), "..", "..", "stadium.db")
        self._init_db()
        logger.info("Database initialized at: %s", self.db_path)

    # ------------------------------------------------------------------
    # Schema
    # ------------------------------------------------------------------
    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.executescript(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT DEFAULT 'fan',
                    language TEXT DEFAULT 'English',
                    preferences TEXT,
                    accessibility_needs TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_active TEXT DEFAULT CURRENT_TIMESTAMP,
                    is_verified INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1
                );
                CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
                CREATE INDEX IF NOT EXISTS idx_users_role  ON users(role);

                CREATE TABLE IF NOT EXISTS stadium_data (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    capacity INTEGER DEFAULT 80000,
                    current_attendance INTEGER DEFAULT 0,
                    event_name TEXT DEFAULT 'FIFA World Cup',
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS crowd_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    section TEXT NOT NULL,
                    density REAL DEFAULT 0,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS queue_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    establishment TEXT NOT NULL,
                    queue_length INTEGER DEFAULT 0,
                    wait_time INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'available',
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS emergency_alerts (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    severity TEXT DEFAULT 'medium',
                    location TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'active',
                    reported_by TEXT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    resolved_at TEXT
                );
                """
            )
            # Idempotent column add for legacy DBs.
            try:
                cur.execute("ALTER TABLE users ADD COLUMN accessibility_needs TEXT")
            except sqlite3.OperationalError:
                pass
            conn.commit()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _parse_json(value: Optional[str]) -> Dict[str, Any]:
        if not value:
            return {}
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return {}

    @staticmethod
    def _parse_json_list(value: Optional[str]) -> List[Any]:
        if not value:
            return []
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return []

    def _row_to_user(self, row: sqlite3.Row) -> Dict[str, Any]:
        user = dict(row)
        user["preferences"] = self._parse_json(user.get("preferences"))
        user["accessibility_needs"] = self._parse_json_list(user.get("accessibility_needs"))
        return user

    # ------------------------------------------------------------------
    # User CRUD
    # ------------------------------------------------------------------
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        return self._row_to_user(row) if row else None

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return self._row_to_user(row) if row else None

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        now_iso = datetime.now(timezone.utc).isoformat()
        with self.get_connection() as conn:
            conn.execute(
                """
                INSERT INTO users (
                    id, name, email, password_hash, role, language,
                    preferences, accessibility_needs, created_at, last_active,
                    is_verified, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_data.get("id"),
                    user_data.get("name"),
                    user_data.get("email"),
                    user_data.get("password_hash"),
                    user_data.get("role", "fan"),
                    user_data.get("language", "English"),
                    json.dumps(user_data.get("preferences", {})),
                    json.dumps(user_data.get("accessibility_needs", [])),
                    user_data.get("created_at", now_iso),
                    user_data.get("last_active", now_iso),
                    1 if user_data.get("is_verified") else 0,
                    1 if user_data.get("is_active", 1) else 0,
                ),
            )
            conn.commit()
        return user_data

    async def update_user(
        self, user_id: str, user_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        allowed = {"name", "language", "preferences", "accessibility_needs", "password_hash"}
        updates: List[str] = []
        values: List[Any] = []
        for key, value in user_data.items():
            if key not in allowed:
                continue
            updates.append(f"{key} = ?")
            values.append(json.dumps(value) if key in {"preferences", "accessibility_needs"} else value)

        if updates:
            values.append(user_id)
            with self.get_connection() as conn:
                conn.execute(
                    f"UPDATE users SET {', '.join(updates)}, last_active = CURRENT_TIMESTAMP "
                    "WHERE id = ?",
                    values,
                )
                conn.commit()
        return await self.get_user_by_id(user_id)

    async def check_connection(self) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("SELECT 1")
            return True
        except sqlite3.Error as exc:
            logger.warning("DB health check failed: %s", exc)
            return False

    async def close_connection(self) -> None:
        # SQLite connections are opened per-call; nothing to do.
        return None