#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lab 1.4 — นำเข้า thailand_road_accidents_2568.csv เข้า SQLite

วิธีใช้:
  python import_road_accidents.py
  python import_road_accidents.py --csv "D:/BigData/thailand_road_accidents_2568.csv"
  python import_road_accidents.py --from-school-db

ถ้าไม่มีไฟล์ CSV จะคัดลอกจาก data/school_data.db (ตัวอย่าง 5,000 แถว)
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_ROOT.parents[1]
DEFAULT_CSV = REPO_ROOT / "data" / "thailand_road_accidents_2568.csv"
SCHOOL_DB = REPO_ROOT / "data" / "school_data.db"
OUTPUT_DB = LAB_ROOT / "output" / "road_accidents.db"
TABLE = "road_accidents"
BATCH = 500


def run_sql_file(conn: sqlite3.Connection, path: Path) -> None:
    sql = path.read_text(encoding="utf-8")
    conn.executescript(sql)


def import_csv(conn: sqlite3.Connection, csv_path: Path) -> int:
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)
        placeholders = ",".join("?" * len(headers))
        col_list = ",".join(f'"{c}"' for c in headers)
        sql = f'INSERT INTO {TABLE} ({col_list}) VALUES ({placeholders})'

        batch: list[list[str]] = []
        total = 0
        for row in reader:
            batch.append(row)
            if len(batch) >= BATCH:
                conn.executemany(sql, batch)
                total += len(batch)
                batch.clear()
        if batch:
            conn.executemany(sql, batch)
            total += len(batch)
    return total


def create_table_from_csv(conn: sqlite3.Connection, csv_path: Path) -> None:
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        headers = next(csv.reader(f))
    cols = ", ".join(f'"{h}" TEXT' for h in headers)
    conn.execute(f"DROP TABLE IF EXISTS {TABLE}")
    conn.execute(f"CREATE TABLE {TABLE} ({cols})")


def copy_from_school_db(conn: sqlite3.Connection, source: Path) -> int:
    if not source.is_file():
        raise FileNotFoundError(f"ไม่พบ {source}")
    src = sqlite3.connect(source)
    try:
        count = src.execute(f"SELECT COUNT(*) FROM {TABLE}").fetchone()[0]
        ddl = src.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
            (TABLE,),
        ).fetchone()
        if not ddl or not ddl[0]:
            raise RuntimeError(f"ตาราง {TABLE} ไม่มีใน {source}")
        conn.executescript(ddl[0])
        rows = src.execute(f"SELECT * FROM {TABLE}").fetchall()
        cols = [d[0] for d in src.execute(f"PRAGMA table_info({TABLE})").fetchall()]
        col_list = ",".join(f'"{c}"' for c in cols)
        placeholders = ",".join("?" * len(cols))
        conn.executemany(
            f"INSERT INTO {TABLE} ({col_list}) VALUES ({placeholders})",
            rows,
        )
        return count
    finally:
        src.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="นำเข้าข้อมูลอุบัติเหตุเข้า SQLite")
    parser.add_argument(
        "--csv",
        type=Path,
        default=DEFAULT_CSV,
        help="path ไปยัง thailand_road_accidents_2568.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DB,
        help="ไฟล์ .db ที่จะสร้าง",
    )
    parser.add_argument(
        "--from-school-db",
        action="store_true",
        help="คัดลอกจาก data/school_data.db แทน CSV",
    )
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        args.output.unlink()

    conn = sqlite3.connect(args.output)
    try:
        if args.from_school_db or not args.csv.is_file():
            if args.csv.is_file() and not args.from_school_db:
                print(f"ไม่พบ CSV ที่ {args.csv} — ใช้ {SCHOOL_DB} แทน")
            n = copy_from_school_db(conn, SCHOOL_DB)
            source = "school_data.db"
        else:
            create_table_from_csv(conn, args.csv)
            n = import_csv(conn, args.csv)
            source = str(args.csv)
        conn.commit()
        ncol = len(conn.execute(f"PRAGMA table_info({TABLE})").fetchall())
        print(f"สำเร็จ: {args.output}")
        print(f"  แหล่งข้อมูล: {source}")
        print(f"  แถว: {n:,} | คอลัมน์: {ncol}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
