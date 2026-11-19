import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / "autopatch.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_code TEXT NOT NULL,
            language TEXT NOT NULL DEFAULT 'python',
            repair_mode TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER NOT NULL,
            bug_type TEXT,
            line_number INTEGER,
            message TEXT,
            FOREIGN KEY(submission_id) REFERENCES submissions(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS repairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER NOT NULL,
            fixed_code TEXT,
            bug_analysis TEXT,
            explanation TEXT,
            retry_count INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(submission_id) REFERENCES submissions(id)
                ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS validations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER NOT NULL,
            success INTEGER NOT NULL,
            output TEXT,
            error TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(submission_id) REFERENCES submissions(id)
                ON DELETE CASCADE
        );
        """)


def save_submission(original_code, repair_mode, bugs=None, fixed_code=None,
                    bug_analysis="", explanation="", retry_count=0,
                    validation=None, status=None):
    bugs = bugs or []
    validation = validation or {}
    now = datetime.now(timezone.utc).isoformat()
    final_status = status or (
        "passed" if validation.get("success") else
        "failed" if validation else "analyzed"
    )

    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO submissions
               (original_code, language, repair_mode, status, created_at)
               VALUES (?, 'python', ?, ?, ?)""",
            (original_code, repair_mode, final_status, now)
        )
        submission_id = cur.lastrowid

        for bug in bugs:
            if not isinstance(bug, dict):
                continue
            conn.execute(
                """INSERT INTO bugs
                   (submission_id, bug_type, line_number, message)
                   VALUES (?, ?, ?, ?)""",
                (
                    submission_id,
                    str(bug.get("type", "Unknown")),
                    bug.get("line", bug.get("line_number")),
                    str(bug.get("message", ""))
                )
            )

        if fixed_code is not None:
            conn.execute(
                """INSERT INTO repairs
                   (submission_id, fixed_code, bug_analysis, explanation, retry_count)
                   VALUES (?, ?, ?, ?, ?)""",
                (submission_id, fixed_code, bug_analysis, explanation, retry_count)
            )

        if validation:
            conn.execute(
                """INSERT INTO validations
                   (submission_id, success, output, error, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    submission_id,
                    int(bool(validation.get("success"))),
                    str(validation.get("output", "")),
                    str(validation.get("error", "")),
                    now
                )
            )
    return submission_id


def get_history(limit=50):
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT s.id, s.original_code, s.language, s.repair_mode,
                   s.status, s.created_at,
                   r.fixed_code, r.bug_analysis, r.explanation, r.retry_count,
                   v.success AS validation_success, v.output, v.error
            FROM submissions s
            LEFT JOIN repairs r ON r.submission_id = s.id
            LEFT JOIN validations v ON v.submission_id = s.id
            ORDER BY s.id DESC
            LIMIT ?
            """,
            (max(1, min(int(limit), 200)),)
        ).fetchall()

        result = []
        for row in rows:
            item = dict(row)
            bug_rows = conn.execute(
                """SELECT bug_type, line_number, message
                   FROM bugs WHERE submission_id = ? ORDER BY id""",
                (item["id"],)
            ).fetchall()
            item["bugs"] = [dict(b) for b in bug_rows]
            result.append(item)
        return result


def get_submission(submission_id):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT s.id, s.original_code, s.language, s.repair_mode,
                   s.status, s.created_at,
                   r.fixed_code, r.bug_analysis, r.explanation, r.retry_count,
                   v.success AS validation_success, v.output, v.error
            FROM submissions s
            LEFT JOIN repairs r ON r.submission_id = s.id
            LEFT JOIN validations v ON v.submission_id = s.id
            WHERE s.id = ?
            """,
            (submission_id,)
        ).fetchone()
        if row is None:
            return None
        item = dict(row)
        bugs = conn.execute(
            """SELECT bug_type, line_number, message
               FROM bugs WHERE submission_id = ? ORDER BY id""",
            (submission_id,)
        ).fetchall()
        item["bugs"] = [dict(b) for b in bugs]
        return item


initialize_database()
