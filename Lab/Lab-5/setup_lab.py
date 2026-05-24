#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""เตรียม Lab หน่วยที่ 5 — JSON, SQLite, MongoDB (fallback)"""

from __future__ import annotations

import csv
import json
import shutil
import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parent
DATA = LAB_ROOT / "data"
OUTPUT = LAB_ROOT / "output"
REPO_ROOT = LAB_ROOT.parents[1]
CSV_PATH = REPO_ROOT / "data" / "thailand_road_accidents_2568.csv"
ROAD_SOURCES = [
    LAB_ROOT.parent / "Lab-2" / "output" / "road_accidents.db",
    LAB_ROOT.parent / "Lab-3" / "output" / "road_accidents.db",
]


def build_sample_api_json(n: int = 50) -> Path:
    out = DATA / "sample_api_data.json"
    DATA.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []

    if CSV_PATH.is_file():
        with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= n:
                    break
                rows.append(
                    {
                        "accident_id": row.get("accident_id", ""),
                        "วันที่": row.get("วันที่เกิดเหตุ", ""),
                        "จังหวัด": row.get("จังหวัด", ""),
                        "ความรุนแรง": row.get("ความรุนแรง", ""),
                        "ยานพาหนะ": row.get("ประเภทยานพาหนะหลัก", ""),
                        "ผู้เสียชีวิต": int(float(row.get("จำนวนผู้เสียชีวิต") or 0)),
                        "ผู้บาดเจ็บ": int(float(row.get("จำนวนผู้บาดเจ็บ") or 0)),
                    }
                )
    else:
        for i in range(1, n + 1):
            rows.append(
                {
                    "accident_id": f"ACC2568{900000 + i:06d}",
                    "วันที่": "2568-01-15",
                    "จังหวัด": "เชียงใหม่",
                    "ความรุนแรง": "ไม่บาดเจ็บ",
                    "ยานพาหนะ": "รถจักรยานยนต์",
                    "ผู้เสียชีวิต": 0,
                    "ผู้บาดเจ็บ": 1,
                }
            )

    with out.open("w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    return out


def build_nested_json() -> Path:
    out = DATA / "sample_nested_accidents.json"
    sample = [
        {
            "accident_id": "ACC2568000001",
            "สถานที่": {"จังหวัด": "สมุทรสาคร", "ภูมิภาค": "ภาคกลาง"},
            "ผู้เสียชีวิต": 0,
            "ผู้เกี่ยวข้อง": [
                {"บทบาท": "คนขับ", "อายุ": 32, "อาการ": "บาดเจ็บ"},
                {"บทบาท": "ผู้โดยสาร", "อายุ": 25, "อาการ": "ไม่บาดเจ็บ"},
            ],
        },
        {
            "accident_id": "ACC2568000002",
            "สถานที่": {"จังหวัด": "เชียงใหม่", "ภูมิภาค": "ภาคเหนือ"},
            "ผู้เสียชีวิต": 1,
            "ผู้เกี่ยวข้อง": [
                {"บทบาท": "คนขับ", "อายุ": 45, "อาการ": "บาดเจ็บสาหัส"},
            ],
        },
    ]
    with out.open("w", encoding="utf-8") as f:
        json.dump(sample, f, ensure_ascii=False, indent=2)
    return out


def copy_road_db() -> Path | None:
    dest = OUTPUT / "school_data.db"
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for src in ROAD_SOURCES:
        if src.is_file():
            shutil.copy2(src, dest)
            return dest
    return None


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "mongo_collections").mkdir(exist_ok=True)

    api = build_sample_api_json(50)
    nested = build_nested_json()
    db = copy_road_db()

    print("เตรียม Lab 5 สำเร็จ:\n")
    print(f"  {api.relative_to(LAB_ROOT)} ({len(json.loads(api.read_text(encoding='utf-8')))} รายการ)")
    print(f"  {nested.relative_to(LAB_ROOT)}")
    if db:
        print(f"  {db.relative_to(LAB_ROOT)} (สำหรับ accidents_api)")
    print(f"  output/mongo_collections/ (โหมดออฟไลน์แทน MongoDB)")
    print("\nขั้นตอนถัดไป:")
    print("  python Lab5-2_json/json_to_sqlite.py")
    print("  python Lab5-3_mongodb/products_crud.py")
    print("  python Lab5-4_pipeline/dashboard_pipeline.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
