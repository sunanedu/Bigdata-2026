#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lab 4.2 — จำลอง Access Control บน SQLite (แทน GRANT/REVOKE)

SQLite ไม่รองรับ GRANT — สคริปต์นี้ตรวจ role ก่อนรัน query
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
DB = LAB_ROOT / "output" / "school_security.db"

ROLE_PERMISSIONS = {
    "admin": {"students", "grades", "subjects", "schedule", "teachers", "audit_log", "users"},
    "teacher": {"students", "grades", "subjects", "schedule", "teachers"},
    "student": {"subjects", "schedule", "grades_own"},
    "parent": {"subjects", "grades_child"},
}


def query_as_role(role: str, sql: str, params: tuple = ()) -> list:
    table = _guess_table(sql)
    if not _allowed(role, table):
        raise PermissionError(f"role '{role}' ไม่มีสิทธิ์เข้าตาราง '{table}'")
    conn = sqlite3.connect(DB)
    try:
        return conn.execute(sql, params).fetchall()
    finally:
        conn.close()


def _guess_table(sql: str) -> str:
    lower = sql.lower()
    if "v_grades_child" in lower:
        return "grades_child"
    if "v_grades" in lower:
        return "grades_own"
    for name in ("teachers", "students", "grades", "subjects", "schedule", "audit_log", "users"):
        if name in lower:
            return name
    return "unknown"


def _allowed(role: str, table: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, set())
    if table in perms:
        return True
    if table == "grades" and "grades" in perms:
        return True
    return False


def demo() -> None:
    print("=== Lab 4.2 Access Control Demo ===\n")
    cases = [
        ("teacher", "SELECT full_name FROM students LIMIT 3", ()),
        ("student", "SELECT subject_name FROM subjects", ()),
        ("student", "SELECT salary FROM teachers LIMIT 1", ()),
        ("parent", "SELECT score FROM v_grades_child_daeng", ()),
    ]
    for role, sql, params in cases:
        print(f"[{role}] {sql[:50]}...")
        try:
            rows = query_as_role(role, sql, params)
            print(f"  OK — {len(rows)} แถว\n")
        except PermissionError as e:
            print(f"  DENIED — {e}\n")


if __name__ == "__main__":
    if not DB.is_file():
        print("รัน python setup_lab.py ก่อน")
        sys.exit(1)
    demo()
