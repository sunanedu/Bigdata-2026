#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline ทำความสะอาด road_accidents (ตามเอกสารบท 3.3)
อ่านจาก CSV หรือ SQLite → บันทึก road_accidents_cleaned.csv
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_ROOT.parents[1]
CSV_PATH = REPO_ROOT / "data" / "thailand_road_accidents_2568_fix.csv"
DB_PATH = LAB_ROOT / "output" / "road_accidents.db"
OUT_DIR = LAB_ROOT / "output"
CLEAN_CSV = OUT_DIR / "road_accidents_cleaned.csv"


def load_dataframe():
    import pandas as pd

    if CSV_PATH.is_file():
        return pd.read_csv(CSV_PATH, encoding="utf-8-sig"), str(CSV_PATH.name)
    if DB_PATH.is_file():
        conn = sqlite3.connect(DB_PATH)
        try:
            df = pd.read_sql_query("SELECT * FROM road_accidents", conn)
        finally:
            conn.close()
        return df, "road_accidents.db"
    raise FileNotFoundError("ไม่พบ CSV หรือ road_accidents.db")


def main() -> int:
    try:
        import pandas as pd
    except ImportError:
        print("pip install pandas")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df, source = load_dataframe()
    n0 = len(df)
    print(f"โหลดสำเร็จจาก {source}: {n0:,} แถว, {df.shape[1]} คอลัมน์")

    null_before = int(df.isnull().sum().sum())
    print(f"NULL ทั้งหมดก่อนทำความสะอาด: {null_before:,}")

    if "อายุ_ปี" in df.columns:
        df["อายุ_ปี"] = pd.to_numeric(df["อายุ_ปี"], errors="coerce")
        df["อายุ_ปี"] = df["อายุ_ปี"].fillna(df["อายุ_ปี"].median())
    if "หมายเลขถนน" in df.columns:
        df["หมายเลขถนน"] = df["หมายเลขถนน"].fillna("ไม่มีหมายเลข")

    dup = int(df.duplicated(subset=["accident_id"]).sum()) if "accident_id" in df.columns else 0
    if dup:
        df = df.drop_duplicates(subset=["accident_id"])
        print(f"ลบ accident_id ซ้ำ: {dup} แถว")

    text_cols = ["จังหวัด", "ภูมิภาค", "ประเภทยานพาหนะหลัก", "ความรุนแรง"]
    for col in text_cols:
        if col in df.columns and df[col].dtype == object:
            df[col] = df[col].str.strip()

    if "วันที่เกิดเหตุ" in df.columns:
        df["วันที่เกิดเหตุ"] = pd.to_datetime(df["วันที่เกิดเหตุ"], errors="coerce")

    df["อายุ_ปี"] = pd.to_numeric(df.get("อายุ_ปี"), errors="coerce")
    df["เดือน"] = pd.to_numeric(df.get("เดือน"), errors="coerce")
    speed_col = "ความเร็วโดยประมาณ_กมชม"
    if speed_col in df.columns:
        df[speed_col] = pd.to_numeric(df[speed_col], errors="coerce")

    mask = df["อายุ_ปี"].between(5, 100) & df["เดือน"].between(1, 12)
    if speed_col in df.columns:
        mask &= df[speed_col].between(10, 200)
    df_clean = df[mask]
    removed = n0 - len(df_clean)
    print(f"กรอง Outlier / ช่วงค่า: ตัด {removed:,} แถว")

    df_clean.to_csv(CLEAN_CSV, index=False, encoding="utf-8-sig")
    print(f"บันทึก {CLEAN_CSV} ({len(df_clean):,} แถว)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
