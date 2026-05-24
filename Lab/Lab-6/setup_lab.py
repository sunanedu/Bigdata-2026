#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เตรียม Lab หน่วยที่ 6 — school_data.db + Chart.js + คัดลอกไป mini project"""

from __future__ import annotations

import importlib.util
import shutil
import sqlite3
import sys
import urllib.request
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent
OUTPUT = LAB_ROOT / "output"
MINI = LAB_ROOT / "Lab6-mini_project"
STATIC = MINI / "static"
REPO_ROOT = LAB_ROOT.parents[1]
JOIN = LAB_ROOT.parent / "Lab-2" / "Lab2-3_join"
ROAD_SOURCES = [
    LAB_ROOT.parent / "Lab-2" / "output" / "road_accidents.db",
    LAB_ROOT.parent / "Lab-3" / "output" / "road_accidents.db",
    LAB_ROOT.parent / "Lab-1" / "output" / "road_accidents.db",
]
CHART_URL = "https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"


def run_sql(conn: sqlite3.Connection, path: Path) -> None:
    conn.executescript(path.read_text(encoding="utf-8"))


def find_road_db() -> Path | None:
    for p in ROAD_SOURCES:
        if p.is_file():
            return p
    return None


def import_road_from_csv(dest: Path) -> bool:
    csv_path = REPO_ROOT / "data" / "thailand_road_accidents_2568.csv"
    if not csv_path.is_file():
        return False
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
    return True


def add_school_tables(conn: sqlite3.Connection) -> None:
    if conn.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='students'"
    ).fetchone()[0]:
        return
    run_sql(conn, JOIN / "schema.sql")
    run_sql(conn, JOIN / "seed.sql")


def build_school_data_db() -> Path:
    dest = OUTPUT / "school_data.db"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()

    road = find_road_db()
    if road:
        shutil.copy2(road, dest)
    elif not import_road_from_csv(dest):
        raise FileNotFoundError("ไม่พบ road_accidents — รัน Lab-1/2 setup ก่อน")

    conn = sqlite3.connect(dest)
    try:
        add_school_tables(conn)
        conn.commit()
    finally:
        conn.close()
    return dest


def download_chart_js() -> Path | None:
    STATIC.mkdir(parents=True, exist_ok=True)
    target = STATIC / "chart.min.js"
    if target.is_file() and target.stat().st_size > 10000:
        return target
    try:
        urllib.request.urlretrieve(CHART_URL, target)
        return target
    except Exception as exc:
        print(f"  คำเตือน: ดาวน์โหลด Chart.js ไม่สำเร็จ ({exc})")
        print("  คัดลอก chart.min.js จากแฟลชไดร์ฟไปที่ Lab6-mini_project/static/")
        return None


def deploy_to_mini_project(db: Path) -> None:
    shutil.copy2(db, MINI / "school_data.db")


def main() -> int:
    MINI.mkdir(parents=True, exist_ok=True)
    db = build_school_data_db()
    deploy_to_mini_project(db)
    chart = download_chart_js()

    conn = sqlite3.connect(db)
    tables = [
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
    ]
    n_road = conn.execute("SELECT COUNT(*) FROM road_accidents").fetchone()[0]
    conn.close()

    print("เตรียม Lab 6 สำเร็จ:\n")
    print(f"  output/school_data.db — {n_road:,} แถว road_accidents")
    print(f"  ตาราง: {', '.join(tables)}")
    print(f"  Lab6-mini_project/school_data.db")
    if chart:
        print(f"  {chart.relative_to(LAB_ROOT)}")
    print("\nขั้นตอนถัดไป:")
    print("  pip install flask")
    print("  python Lab6-2_flask/hello_flask.py")
    print("  cd Lab6-mini_project && python app.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
