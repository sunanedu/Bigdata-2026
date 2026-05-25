#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""สร้างฐานข้อมูลและเตรียม Lab หน่วยที่ 2"""

from __future__ import annotations

import shutil
import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent
OUTPUT = LAB_ROOT / "output"
REPO_ROOT = LAB_ROOT.parents[1]
LAB1_OUTPUT = LAB_ROOT.parent / "Lab-1" / "output" / "road_accidents.db"
CSV_PATH = REPO_ROOT / "data" / "thailand_road_accidents_2568_fix.csv"


def run_script(conn: sqlite3.Connection, path: Path) -> None:
    conn.executescript(path.read_text(encoding="utf-8"))


def build_db(name: str, schema: Path, seed: Path | None = None) -> Path:
    db = OUTPUT / name
    if db.exists():
        db.unlink()
    conn = sqlite3.connect(db)
    try:
        run_script(conn, schema)
        if seed and seed.is_file():
            run_script(conn, seed)
        conn.commit()
    finally:
        conn.close()
    return db


def ensure_road_accidents() -> Path:
    dest = OUTPUT / "road_accidents.db"
    if dest.exists():
        dest.unlink()

    if LAB1_OUTPUT.is_file():
        shutil.copy2(LAB1_OUTPUT, dest)
        return dest

    if CSV_PATH.is_file():
        import importlib.util

        lab1_import = REPO_ROOT / "Lab" / "Lab-1" / "Lab1-4_csv_import" / "import_road_accidents.py"
        spec = importlib.util.spec_from_file_location("import_road", lab1_import)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        mod.OUTPUT_DB = dest
        conn = sqlite3.connect(dest)
        try:
            mod.create_table_from_csv(conn, CSV_PATH)
            mod.import_csv(conn, CSV_PATH)
            conn.commit()
        finally:
            conn.close()
        return dest

    school = REPO_ROOT / "data" / "school_data.db"
    if school.is_file():
        import importlib.util

        lab1_import = REPO_ROOT / "Lab" / "Lab-1" / "Lab1-4_csv_import" / "import_road_accidents.py"
        spec = importlib.util.spec_from_file_location("import_road", lab1_import)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        conn = sqlite3.connect(dest)
        try:
            mod.copy_from_school_db(conn, school)
            conn.commit()
        finally:
            conn.close()
        return dest

    raise FileNotFoundError(
        "ไม่พบ road_accidents — รัน Lab-1/setup_lab.py หรือวาง CSV ที่ data/"
    )


def apply_views(db_path: Path) -> None:
    views = LAB_ROOT / "Lab2-4_view_index_transaction" / "views.sql"
    conn = sqlite3.connect(db_path)
    try:
        run_script(conn, views)
        conn.commit()
    finally:
        conn.close()


def build_bank_demo() -> Path:
    db = OUTPUT / "bank_demo.db"
    if db.exists():
        db.unlink()
    conn = sqlite3.connect(db)
    try:
        conn.executescript(
            """
            CREATE TABLE bank_accounts (
                account_id TEXT PRIMARY KEY,
                owner_name TEXT NOT NULL,
                balance    REAL NOT NULL CHECK(balance >= 0)
            );
            INSERT INTO bank_accounts VALUES
                ('ACC001', 'สมชาย', 10000),
                ('ACC002', 'สมหญิง', 5000);
            """
        )
        conn.commit()
    finally:
        conn.close()
    return db


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "exports").mkdir(exist_ok=True)

    dbs = [
        build_db(
            "ddl_students.db",
            LAB_ROOT / "Lab2-1_ddl_dml" / "workshop.sql",
        ),
        ensure_road_accidents(),
        build_db(
            "school_join.db",
            LAB_ROOT / "Lab2-3_join" / "schema.sql",
            LAB_ROOT / "Lab2-3_join" / "seed.sql",
        ),
        build_bank_demo(),
    ]

    apply_views(dbs[1])

    print("สร้างฐานข้อมูล Lab 2 สำเร็จ:\n")
    for p in dbs:
        if p.suffix == ".db":
            kb = p.stat().st_size / 1024
            print(f"  {p.relative_to(LAB_ROOT)} ({kb:.1f} KB)")

    conn = sqlite3.connect(dbs[1])
    n = conn.execute("SELECT COUNT(*) FROM road_accidents").fetchone()[0]
    views = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='view'"
    ).fetchall()
    conn.close()
    print(f"\nroad_accidents: {n:,} แถว | VIEW: {[v[0] for v in views]}")

    print("\nขั้นตอนถัดไป:")
    print("  DB Browser → เปิดไฟล์ใน output/")
    print("  python Lab2-5_python_pipeline/pipeline.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
