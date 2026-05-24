#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เตรียม Lab หน่วยที่ 4"""

from __future__ import annotations

import importlib.util
import shutil
import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent
OUTPUT = LAB_ROOT / "output"
REPO_ROOT = LAB_ROOT.parents[1]
AC = LAB_ROOT / "Lab4-2_access_control"
ROAD_SOURCES = [
    LAB_ROOT.parent / "Lab-2" / "output" / "road_accidents.db",
    LAB_ROOT.parent / "Lab-3" / "output" / "road_accidents.db",
    LAB_ROOT.parent / "Lab-1" / "output" / "road_accidents.db",
]

PASSWORDS = {
    "admin_it": "Adm1n#Sup3r!",
    "teacher_wichai": "T3ach3r#2026",
    "student_somjai": "St4d3nt#2026",
    "parent_daeng": "P4r3nt#2026",
}


def run_sql(conn: sqlite3.Connection, path: Path) -> None:
    conn.executescript(path.read_text(encoding="utf-8"))


def hash_password_with_salt(password: str) -> tuple[str, str]:
    spec = importlib.util.spec_from_file_location(
        "ph", LAB_ROOT / "Lab4-4_security_tech" / "password_hash.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod.hash_password_with_salt(password)


def build_school_security() -> Path:
    db = OUTPUT / "school_security.db"
    if db.exists():
        db.unlink()
    conn = sqlite3.connect(db)
    try:
        run_sql(conn, AC / "schema.sql")
        run_sql(conn, AC / "seed.sql")
        run_sql(conn, AC / "views.sql")
        for username, plain in PASSWORDS.items():
            salt, hashed = hash_password_with_salt(plain)
            conn.execute(
                "UPDATE users SET salt = ?, password_hash = ? WHERE username = ?",
                (salt, hashed, username),
            )
        conn.commit()
    finally:
        conn.close()
    return db


def ensure_road_accidents() -> Path | None:
    dest = OUTPUT / "road_accidents.db"
    if dest.exists():
        dest.unlink()
    for src in ROAD_SOURCES:
        if src.is_file():
            shutil.copy2(src, dest)
            return dest
    csv_path = REPO_ROOT / "data" / "thailand_road_accidents_2568.csv"
    if csv_path.is_file():
        mod_path = REPO_ROOT / "Lab" / "Lab-1" / "Lab1-4_csv_import" / "import_road_accidents.py"
        spec = importlib.util.spec_from_file_location("imp", mod_path)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        conn = sqlite3.connect(dest)
        try:
            mod.create_table_from_csv(conn, csv_path)
            mod.import_csv(conn, csv_path)
            conn.commit()
        finally:
            conn.close()
        return dest
    return None


def seed_audit_samples(db: Path) -> None:
    spec = importlib.util.spec_from_file_location(
        "al", LAB_ROOT / "Lab4-4_security_tech" / "audit_log.py"
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    mod.log_action(db, "teacher_wichai", "UPDATE", "grades", "G001", {"score": 55}, {"score": 65})
    mod.log_action(
        db,
        "student_somjai",
        "SELECT",
        "teachers",
        status="FAILED - Permission Denied",
    )


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "backups").mkdir(exist_ok=True)

    school = build_school_security()
    seed_audit_samples(school)
    road = ensure_road_accidents()

    print("เตรียม Lab 4 สำเร็จ:\n")
    print(f"  {school.relative_to(LAB_ROOT)}")
    if road:
        n = sqlite3.connect(road).execute("SELECT COUNT(*) FROM road_accidents").fetchone()[0]
        print(f"  {road.relative_to(LAB_ROOT)} ({n:,} แถว)")
    print("\nรหัสผ่านทดสอบ (เก็บเป็น Hash ใน DB):")
    for u, p in PASSWORDS.items():
        print(f"  {u} / {p}")
    print("\nขั้นตอนถัดไป:")
    print("  python Lab4-4_security_tech/workshop_4_4.py")
    print("  python Lab4-2_access_control/access_control.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
