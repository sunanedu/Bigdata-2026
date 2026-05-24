#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้างฐานข้อมูลทั้งหมดสำหรับ Lab หน่วยที่ 1 ไว้ในโฟลเดอร์ output/

  python setup_lab.py
"""

from __future__ import annotations

import csv
import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent
OUTPUT = LAB_ROOT / "output"
DATA = LAB_ROOT / "data"
REPO_DATA = LAB_ROOT.parents[1] / "data"


def run_script(conn: sqlite3.Connection, path: Path) -> None:
    conn.executescript(path.read_text(encoding="utf-8"))


def build_db(name: str, schema: Path, seed: Path | None = None) -> Path:
    db_path = OUTPUT / name
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    try:
        run_script(conn, schema)
        if seed and seed.is_file():
            run_script(conn, seed)
        conn.commit()
    finally:
        conn.close()
    return db_path


def import_students_csv(conn: sqlite3.Connection, csv_path: Path) -> None:
    conn.execute("DROP TABLE IF EXISTS students")
    conn.execute(
        """
        CREATE TABLE students (
            student_id TEXT PRIMARY KEY,
            name       TEXT NOT NULL,
            grade      INTEGER,
            gpa        REAL,
            birthdate  TEXT
        )
        """
    )
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                r["student_id"],
                r["name"],
                int(r["grade"]),
                float(r["gpa"]),
                r.get("birthdate", ""),
            )
            for r in reader
        ]
    conn.executemany(
        "INSERT INTO students VALUES (?,?,?,?,?)",
        rows,
    )


def build_school_system() -> Path:
    """ฐานข้อมูลโรงเรียน (students + subjects + enrollments) สำหรับหน่วยที่ 2"""
    db_path = OUTPUT / "school_system.db"
    if db_path.exists():
        db_path.unlink()
    conn = sqlite3.connect(db_path)
    try:
        import_students_csv(conn, DATA / "students.csv")
        conn.executescript(
            """
            CREATE TABLE subjects (
                subj_id   TEXT PRIMARY KEY,
                subj_name TEXT NOT NULL,
                credits   INTEGER,
                teacher   TEXT
            );

            CREATE TABLE enrollments (
                enroll_id TEXT PRIMARY KEY,
                std_id    TEXT NOT NULL REFERENCES students(student_id),
                subj_id   TEXT NOT NULL REFERENCES subjects(subj_id),
                score     REAL,
                semester  TEXT
            );

            INSERT INTO subjects VALUES
                ('MAT101', 'คณิตศาสตร์', 3, 'ครูสมศักดิ์'),
                ('ENG101', 'ภาษาอังกฤษ', 3, 'ครูสมบัติ'),
                ('SCI101', 'วิทยาศาสตร์', 3, 'ครูสมศักดิ์'),
                ('THA101', 'ภาษาไทย', 2, 'ครูวิไล'),
                ('SOC101', 'สังคมศึกษา', 2, 'ครูประเสริฐ');

            INSERT INTO enrollments VALUES
                ('ENR001', 'STU001', 'MAT101', 85, '1/2568'),
                ('ENR002', 'STU001', 'ENG101', 72, '1/2568'),
                ('ENR003', 'STU001', 'SCI101', 90, '1/2568'),
                ('ENR004', 'STU002', 'MAT101', 91, '1/2568'),
                ('ENR005', 'STU002', 'THA101', 88, '1/2568'),
                ('ENR006', 'STU003', 'ENG101', 65, '1/2568'),
                ('ENR007', 'STU004', 'MAT101', 78, '1/2568'),
                ('ENR008', 'STU005', 'SCI101', 82, '1/2568');
            """
        )
        conn.commit()
    finally:
        conn.close()
    return db_path


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)

    dbs = [
        build_db(
            "my_first_database.db",
            LAB_ROOT / "Lab1-2_first_database" / "schema.sql",
            LAB_ROOT / "Lab1-2_first_database" / "seed.sql",
        ),
        build_db(
            "shop_database.db",
            LAB_ROOT / "Lab1-3_shop_erd" / "schema.sql",
            LAB_ROOT / "Lab1-3_shop_erd" / "seed.sql",
        ),
        build_school_system(),
    ]

    # Lab 1.4 — road accidents
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "import_road",
        LAB_ROOT / "Lab1-4_csv_import" / "import_road_accidents.py",
    )
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    mod.OUTPUT_DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(mod.OUTPUT_DB)
    try:
        if mod.DEFAULT_CSV.is_file():
            mod.create_table_from_csv(conn, mod.DEFAULT_CSV)
            n = mod.import_csv(conn, mod.DEFAULT_CSV)
            src = mod.DEFAULT_CSV.name
        else:
            if mod.OUTPUT_DB.exists():
                mod.OUTPUT_DB.unlink()
            conn.close()
            conn = sqlite3.connect(mod.OUTPUT_DB)
            n = mod.copy_from_school_db(conn, mod.SCHOOL_DB)
            src = "school_data.db (ตัวอย่าง)"
        conn.commit()
        dbs.append(mod.OUTPUT_DB)
        print(f"road_accidents.db — {n:,} แถว จาก {src}")
    finally:
        conn.close()

    print("\nสร้างฐานข้อมูล Lab 1 สำเร็จ:")
    for p in dbs:
        size_kb = p.stat().st_size / 1024
        print(f"  {p.relative_to(LAB_ROOT)} ({size_kb:.1f} KB)")

    if REPO_DATA.joinpath("school_data.db").is_file():
        print(f"\nหมายเหตุ: {REPO_DATA / 'school_data.db'} มีอยู่แล้ว (ใช้ในหลักสูตร)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
