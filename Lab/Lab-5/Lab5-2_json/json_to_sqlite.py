#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workshop 5.2 — ดึงข้อมูล JSON → บันทึกลง SQLite
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
API_JSON = LAB_ROOT / "data" / "sample_api_data.json"
DB_PATH = LAB_ROOT / "output" / "school_data.db"


def main() -> int:
    try:
        import pandas as pd
    except ImportError:
        print("pip install pandas")
        return 1

    if not API_JSON.is_file():
        print("รัน python setup_lab.py ก่อน")
        return 1

    print("=== ขั้นที่ 1: อ่าน JSON ===")
    with API_JSON.open(encoding="utf-8") as f:
        raw = json.load(f)
    print(f"จำนวน: {len(raw)} รายการ")

    print("\n=== ขั้นที่ 2: DataFrame ===")
    df = pd.DataFrame(raw)
    print(df.shape)
    print(df.head(3))

    print("\n=== ขั้นที่ 3: ตรวจสอบ ===")
    print(df.isnull().sum())
    print(df.dtypes)

    print("\n=== ขั้นที่ 4: SQLite ===")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("accidents_api", conn, if_exists="replace", index=False)
    print("บันทึกตาราง accidents_api สำเร็จ")

    print("\n=== ขั้นที่ 5: Query ===")
    result = pd.read_sql(
        """
        SELECT accident_id, วันที่, จังหวัด, ผู้เสียชีวิต
        FROM accidents_api
        WHERE ผู้เสียชีวิต > 0
        """,
        conn,
    )
    print(f"พบอุบัติเหตุที่มีผู้เสียชีวิต: {len(result)} ครั้ง")
    print(result.head())
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
