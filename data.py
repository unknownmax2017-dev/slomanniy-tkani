import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List

import sqlite3

DB_FILE = "data.db"


@dataclass
class User:
    id: int
    premium: bool = False
    premium_until: datetime | None = None


class Store:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self._users: Dict[int, User] = {}
        self._reminders: List[dict] = []
        self._conn = sqlite3.connect(db_file, check_same_thread=False)
        self._conn.execute(
            """CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY,
                premium INTEGER DEFAULT 0,
                premium_until TEXT
            )"""
        )
        self._conn.execute(
            """CREATE TABLE IF NOT EXISTS reminders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                due TEXT
            )"""
        )
        self._conn.commit()

    def register(self, user_id: int) -> None:
        row = self._conn.execute(
            "SELECT premium, premium_until FROM users WHERE id=?", (user_id,)
        ).fetchone()
        if row is None:
            self._conn.execute("INSERT INTO users(id, premium, premium_until) VALUES(?,0,?)", (user_id, None))
            self._conn.commit()
        self._users[user_id] = User(user_id, bool(row and row[0]), row[1] if row else None)

    def is_premium(self, user_id: int) -> bool:
        u = self._users.get(user_id) or self._load(user_id)
        if not u:
            return False
        if u.premium and u.premium_until:
            until = datetime.fromisoformat(u.premium_until)
            if until < datetime.now():
                self.set_premium(user_id, False)
                return False
        return bool(u.premium)

    def _load(self, user_id: int) -> User:
        row = self._conn.execute(
            "SELECT premium, premium_until FROM users WHERE id=?", (user_id,)
        ).fetchone()
        u = User(user_id, bool(row and row[0]), row[1] if row else None)
        self._users[user_id] = u
        return u

    def set_premium(self, user_id: int, on: bool, days: int = 0) -> None:
        until = None
        if on:
            until = (datetime.now() + timedelta(days=days)).isoformat() if days else None
        self._conn.execute(
            "UPDATE users SET premium=?, premium_until=? WHERE id=?",
            (1 if on else 0, until, user_id),
        )
        self._conn.commit()
        self._users[user_id] = User(user_id, on, until)

    def add_reminder(self, user_id: int, text: str, seconds: int) -> None:
        due = (datetime.now() + timedelta(seconds=seconds)).isoformat()
        self._conn.execute(
            "INSERT INTO reminders(user_id, text, due) VALUES(?,?,?)", (user_id, text, due)
        )
        self._conn.commit()

    def due_reminders(self) -> List[dict]:
        now = datetime.now().isoformat()
        rows = self._conn.execute(
            "SELECT id, user_id, text, due FROM reminders WHERE due<=?", (now,)
        ).fetchall()
        if rows:
            self._conn.execute("DELETE FROM reminders WHERE due<=?", (now,))
            self._conn.commit()
        return [{"user_id": r[1], "text": r[2]} for r in rows]


store = Store()