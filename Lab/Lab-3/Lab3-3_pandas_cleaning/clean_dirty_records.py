#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workshop 3.3 — ทำความสะอาด dirty_records.csv → clean_records.csv

เกณฑ์ (ตามเอกสาร):
  1. ไม่มี NULL ใน จังหวัด, ความรุนแรง, อายุ_ปี
  2. ไม่มี accident_id ซ้ำ
  3. อายุ_ปี อยู่ระหว่าง 5–100
  4. เดือน อยู่ระหว่าง 1–12
  5. ข้อความไม่มีช่องว่างนำหน้า/ท้าย
"""

from __future__ import annotations

import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = LAB_ROOT / "data"
OUT_DIR = LAB_ROOT / "output"
DIRTY = DATA_DIR / "dirty_records.csv"
CLEAN = OUT_DIR / "clean_records.csv"


def main() -> int:
    try:
        import pandas as pd
    except ImportError:
        print("pip install pandas")
        return 1

    if not DIRTY.is_file():
        print(f"ไม่พบ {DIRTY} — รัน python setup_lab.py")
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DIRTY, encoding="utf-8-sig")
    n0 = len(df)
    print(f"โหลด dirty_records: {n0} แถว")

    for col in ["จังหวัด", "ความรุนแรง", "accident_id"]:
        if col in df.columns and df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": None, "": None})

    df["อายุ_ปี"] = pd.to_numeric(df["อายุ_ปี"], errors="coerce")
    df["เดือน"] = pd.to_numeric(df["เดือน"], errors="coerce")

    df = df.dropna(subset=["จังหวัด", "ความรุนแรง", "อายุ_ปี"])
    df = df.drop_duplicates(subset=["accident_id"], keep="first")
    df = df[df["อายุ_ปี"].between(5, 100)]
    df = df[df["เดือน"].between(1, 12)]

    for col in df.columns:
        if df[col].dtype == object or str(df[col].dtype) == "string":
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace("nan", None)

    df.to_csv(CLEAN, index=False, encoding="utf-8-sig")
    print(f"บันทึก {CLEAN.name}: {len(df)} แถว (ลบ/กรอง {n0 - len(df)} แถว)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
