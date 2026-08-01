# -*- coding: utf-8 -*-
"""
Notların saklandığı basit SQLite veritabanı.
Notion yerine: tüm notlar burada saklanır, /bugun ve /ara komutlarıyla
görüntülenir, .docx olarak dışa aktarılabilir.
"""
import sqlite3
from datetime import datetime, date
from contextlib import contextmanager

DB_PATH = "notes.db"


def init_db():
    with _conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                note_type TEXT NOT NULL,        -- 'vizit' | 'konsultasyon'
                patient_info TEXT NOT NULL,     -- hasta adı / oda no
                transcript TEXT NOT NULL,
                structured_note TEXT NOT NULL,
                telegram_user_id INTEGER NOT NULL
            )
        """)


@contextmanager
def _conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def save_note(note_type: str, patient_info: str, transcript: str,
              structured_note: str, telegram_user_id: int) -> int:
    with _conn() as c:
        cur = c.execute(
            """INSERT INTO notes
               (created_at, note_type, patient_info, transcript,
                structured_note, telegram_user_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (datetime.now().isoformat(), note_type, patient_info,
             transcript, structured_note, telegram_user_id),
        )
        return cur.lastrowid


def get_notes_by_date(target_date: date):
    start = f"{target_date.isoformat()}T00:00:00"
    end = f"{target_date.isoformat()}T23:59:59"
    with _conn() as c:
        cur = c.execute(
            """SELECT id, created_at, note_type, patient_info, structured_note
               FROM notes WHERE created_at BETWEEN ? AND ?
               ORDER BY created_at ASC""",
            (start, end),
        )
        return cur.fetchall()


def search_notes_by_patient(query: str, limit: int = 15):
    with _conn() as c:
        cur = c.execute(
            """SELECT id, created_at, note_type, patient_info, structured_note
               FROM notes WHERE patient_info LIKE ?
               ORDER BY created_at DESC LIMIT ?""",
            (f"%{query}%", limit),
        )
        return cur.fetchall()


def get_note_by_id(note_id: int):
    with _conn() as c:
        cur = c.execute(
            """SELECT id, created_at, note_type, patient_info,
                      transcript, structured_note
               FROM notes WHERE id = ?""",
            (note_id,),
        )
        return cur.fetchone()
