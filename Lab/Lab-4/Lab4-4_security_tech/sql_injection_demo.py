#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workshop 4.4 — SQL Injection สาธิตและป้องกัน
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
DB = LAB_ROOT / "output" / "school_security.db"

sys.path.insert(0, str(Path(__file__).parent))
from password_hash import verify_password  # noqa: E402


def login_unsafe(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB)
    try:
        query = (
            f"SELECT 1 FROM users WHERE username='{username}' "
            f"AND password_hash='{password}'"
        )
        print(f"  [UNSAFE] Query: {query[:80]}...")
        return conn.execute(query).fetchone() is not None
    finally:
        conn.close()


def login_safe(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB)
    try:
        row = conn.execute(
            "SELECT password_hash, salt FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if not row:
            return False
        stored_hash, salt = row
        return verify_password(password, salt, stored_hash)
    finally:
        conn.close()


def search_accidents_safe(province: str, year: int) -> list:
    road_db = LAB_ROOT / "output" / "road_accidents.db"
    if not road_db.is_file():
        return []
    conn = sqlite3.connect(road_db)
    try:
        return conn.execute(
            """
            SELECT accident_id, วันที่เกิดเหตุ, จังหวัด, ความรุนแรง
            FROM road_accidents
            WHERE จังหวัด = ? AND "ปี_พ.ศ." = ?
            LIMIT 5
            """,
            (province, year),
        ).fetchall()
    finally:
        conn.close()


def main() -> int:
    if not DB.is_file():
        print("รัน python setup_lab.py ก่อน")
        return 1

    print("=== SQL Injection Demo ===\n")

    print("1) login_unsafe + injection (username only check — demo):")
    conn = sqlite3.connect(DB)
    try:
        user = "admin_it' --"
        pwd = "anything"
        q = f"SELECT username FROM users WHERE username='{user}'"
        print(f"  Query: {q}")
        got = conn.execute(q).fetchone()
        print(f"  พบ user: {got is not None} (อันตรายถ้าไม่ตรวจ password)\n")
    finally:
        conn.close()

    print("2) login_safe + injection:")
    tests = [
        ("admin_it", "Adm1n#Sup3r!"),
        ("admin_it' --", "x"),
        ("' OR '1'='1' --", "x"),
    ]
    for u, p in tests:
        ok = login_safe(u, p)
        print(f"  login_safe({u!r}, ...): {ok}")

    print("\n3) search_accidents_safe + injection ในชื่อจังหวัด:")
    n = len(search_accidents_safe("'; DROP TABLE road_accidents; --", 2568))
    print(f"  ผลลัพธ์: {n} แถว (ไม่ทำลายตาราง)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
