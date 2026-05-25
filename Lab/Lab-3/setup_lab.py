#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เตรียม Lab หน่วยที่ 3 — ฐานข้อมูล + dirty_records.csv"""

from __future__ import annotations

import csv
import shutil
import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent
OUTPUT = LAB_ROOT / "output"
DATA = LAB_ROOT / "data"
REPO_ROOT = LAB_ROOT.parents[1]
CSV_FULL = REPO_ROOT / "data" / "thailand_road_accidents_2568_fix.csv"
ROAD_DB_SOURCES = [
    LAB_ROOT.parent / "Lab-2" / "output" / "road_accidents.db",
    LAB_ROOT.parent / "Lab-1" / "output" / "road_accidents.db",
]

DIRTY_COLS = [
    "accident_id",
    "วันที่เกิดเหตุ",
    "จังหวัด",
    "ความรุนแรง",
    "อายุ_ปี",
    "เดือน",
    "ความเร็วโดยประมาณ_กมชม",
    "จำกัดความเร็ว_กมชม",
    "เกินความเร็ว_ใช่ไม่ใช่",
    "จำนวนผู้เสียชีวิต",
]


def ensure_road_accidents_db() -> Path:
    dest = OUTPUT / "road_accidents.db"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        dest.unlink()
    for src in ROAD_DB_SOURCES:
        if src.is_file():
            shutil.copy2(src, dest)
            return dest
    if CSV_FULL.is_file():
        import importlib.util

        mod_path = REPO_ROOT / "Lab" / "Lab-1" / "Lab1-4_csv_import" / "import_road_accidents.py"
        spec = importlib.util.spec_from_file_location("import_road", mod_path)
        mod = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(mod)
        conn = sqlite3.connect(dest)
        try:
            mod.create_table_from_csv(conn, CSV_FULL)
            mod.import_csv(conn, CSV_FULL)
            conn.commit()
        finally:
            conn.close()
        return dest
    raise FileNotFoundError("ไม่พบ road_accidents — รัน Lab-1 หรือ Lab-2 setup ก่อน")


def resolve_columns(headers: list[str]) -> list[str]:
    """จับคู่ชื่อคอลัมน์จาก CSV จริง (กัน Unicode ต่างรูปแบบ)"""
    resolved: list[str] = []
    for want in DIRTY_COLS:
        if want in headers:
            resolved.append(want)
            continue
        found = next((h for h in headers if want in h or h in want), None)
        if found:
            resolved.append(found)
    return resolved


def build_dirty_records_csv() -> Path:
    """สร้าง dirty_records.csv ที่มีปัญหาเจตนา ~100 แถว"""
    DATA.mkdir(parents=True, exist_ok=True)
    out = DATA / "dirty_records.csv"

    rows: list[dict] = []
    use_cols = list(DIRTY_COLS)
    if CSV_FULL.is_file():
        with CSV_FULL.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            headers = list(reader.fieldnames or [])
            use_cols = resolve_columns(headers)
            for i, row in enumerate(reader):
                if i >= 100:
                    break
                rows.append({c: row.get(c, "") for c in use_cols})
    else:
        for i in range(1, 101):
            rows.append(
                {
                    "accident_id": f"ACC2568{900000 + i:06d}",
                    "วันที่เกิดเหตุ": "2568-01-15",
                    "จังหวัด": "เชียงใหม่",
                    "ความรุนแรง": "ไม่บาดเจ็บ",
                    "อายุ_ปี": "35",
                    "เดือน": "1",
                    "ความเร็วโดยประมาณ_กมชม": "60",
                    "จำกัดความเร็ว_กมชม": "60",
                    "เกินความเร็ว_ใช่ไม่ใช่": "ไม่ใช่",
                    "จำนวนผู้เสียชีวิต": "0",
                }
            )

    col_map: dict[str, str] = {}
    for want in DIRTY_COLS:
        if want in use_cols:
            col_map[want] = want
        else:
            match = next((c for c in use_cols if want in c or c in want), want)
            col_map[want] = match

    def key(name: str) -> str:
        return col_map.get(name, name)

    def mutate(idx: int, **kwargs) -> None:
        for k, v in kwargs.items():
            rows[idx][key(k)] = v

    if len(rows) >= 20:
        aid = key("accident_id")
        mutate(0, **{aid: rows[1][aid]})
        mutate(2, **{key("อายุ_ปี"): ""})
        mutate(3, **{key("จังหวัด"): ""})
        mutate(4, **{key("ความรุนแรง"): ""})
        mutate(5, **{key("อายุ_ปี"): "-5"})
        mutate(6, **{key("อายุ_ปี"): "150"})
        mutate(7, **{key("เดือน"): "13"})
        mutate(8, **{key("เดือน"): "0"})
        mutate(9, **{key("ความเร็วโดยประมาณ_กมชม"): "350"})
        mutate(10, **{key("ความรุนแรง"): "บาดเจ็บหนักมาก"})
        mutate(
            11,
            **{
                key("เกินความเร็ว_ใช่ไม่ใช่"): "ใช่",
                key("ความเร็วโดยประมาณ_กมชม"): "40",
                key("จำกัดความเร็ว_กมชม"): "60",
            },
        )
        mutate(
            12,
            **{
                key("จำนวนผู้เสียชีวิต"): "2",
                key("ความรุนแรง"): "ไม่บาดเจ็บ",
            },
        )
        mutate(13, **{key("จังหวัด"): " กรุงเทพมหานคร "})
        mutate(14, **{key("จังหวัด"): "กรุงเทพฯ"})
        mutate(15, **{aid: rows[16][aid]})

    with out.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=use_cols)
        writer.writeheader()
        writer.writerows(rows)

    return out


def import_dirty_to_sqlite(csv_path: Path) -> Path:
    db = OUTPUT / "dirty_records.db"
    if db.exists():
        db.unlink()
    conn = sqlite3.connect(db)
    try:
        with csv_path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            headers = next(reader)
            cols = ", ".join(f'"{h}" TEXT' for h in headers)
            conn.execute(f"CREATE TABLE dirty_records ({cols})")
            ph = ",".join("?" * len(headers))
            col_list = ",".join(f'"{h}"' for h in headers)
            conn.executemany(
                f"INSERT INTO dirty_records ({col_list}) VALUES ({ph})",
                list(reader),
            )
        conn.commit()
    finally:
        conn.close()
    return db


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "reports").mkdir(exist_ok=True)

    road = ensure_road_accidents_db()
    n = sqlite3.connect(road).execute("SELECT COUNT(*) FROM road_accidents").fetchone()[0]
    dirty_csv = build_dirty_records_csv()
    dirty_db = import_dirty_to_sqlite(dirty_csv)

    print("เตรียม Lab 3 สำเร็จ:\n")
    print(f"  {road.relative_to(LAB_ROOT)} ({road.stat().st_size / 1024:.0f} KB, {n:,} แถว)")
    print(f"  {dirty_csv.relative_to(LAB_ROOT)} ({dirty_csv.stat().st_size / 1024:.1f} KB)")
    print(f"  {dirty_db.relative_to(LAB_ROOT)}")
    print("\nขั้นตอนถัดไป:")
    print("  DB Browser → workshop_10_checks.sql")
    print("  python Lab3-3_pandas_cleaning/clean_dirty_records.py")
    print("  python Lab3-3_pandas_cleaning/clean_road_accidents.py")
    print("  python Lab3-4_dq_report/generate_dq_report.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
