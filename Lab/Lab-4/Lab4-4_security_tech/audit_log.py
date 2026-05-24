#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit Log — บันทึกการเข้าถึง (บทที่ 4.4)"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

LAB_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = LAB_ROOT / "output" / "school_security.db"


def log_action(
    db_path: Path | str,
    username: str,
    action: str,
    table_name: str,
    record_id: str | None = None,
    old_value: Any = None,
    new_value: Any = None,
    ip_address: str = "127.0.0.1",
    status: str = "SUCCESS",
) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO audit_log
                (username, action, table_name, record_id, old_value, new_value, ip_address, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                action,
                table_name,
                record_id,
                str(old_value) if old_value is not None else None,
                str(new_value) if new_value is not None else None,
                ip_address,
                status,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def show_recent(db_path: Path | str = DEFAULT_DB, limit: int = 10) -> None:
    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(
            """
            SELECT timestamp, username, action, table_name, status
            FROM audit_log
            ORDER BY log_id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    finally:
        conn.close()
    print(f"Audit Log ล่าสุด {limit} รายการ:")
    for r in rows:
        print(f"  {r}")


def demo() -> None:
    db = DEFAULT_DB
    log_action(db, "teacher_wichai", "UPDATE", "grades", "G001", {"score": 55}, {"score": 65})
    log_action(
        db,
        "student_somjai",
        "SELECT",
        "teachers",
        status="FAILED - Permission Denied",
    )
    log_action(db, "admin_it", "LOGIN", "users", status="SUCCESS")
    show_recent(db)


if __name__ == "__main__":
    demo()
