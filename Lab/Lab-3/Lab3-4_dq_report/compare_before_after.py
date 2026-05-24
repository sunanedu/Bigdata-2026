#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Workshop 3.4 — สรุปตาราง ก่อน vs หลัง ทำความสะอาด"""

from __future__ import annotations

import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
DIRTY = LAB_ROOT / "data" / "dirty_records.csv"
CLEAN = LAB_ROOT / "output" / "clean_records.csv"


def metrics(path: Path) -> dict:
    import pandas as pd

    df = pd.read_csv(path, encoding="utf-8-sig")
    age = pd.to_numeric(df.get("อายุ_ปี"), errors="coerce")
    month = pd.to_numeric(df.get("เดือน"), errors="coerce")
    dup = 0
    if "accident_id" in df.columns:
        dup = len(df) - df["accident_id"].nunique()
    null_key = 0
    for c in ["จังหวัด", "ความรุนแรง", "อายุ_ปี"]:
        if c in df.columns:
            null_key += int(df[c].isnull().sum())
    outlier = int(((age < 5) | (age > 100) | (month < 1) | (month > 12)).sum())
    trim_bad = 0
    if "จังหวัด" in df.columns and df["จังหวัด"].dtype == object:
        trim_bad = int((df["จังหวัด"] != df["จังหวัด"].str.strip()).sum())
    return {
        "rows": len(df),
        "null_key": null_key,
        "dup_id": dup,
        "outlier": outlier,
        "trim": trim_bad,
    }


def main() -> int:
    if not DIRTY.is_file() or not CLEAN.is_file():
        print("รัน setup_lab.py และ clean_dirty_records.py ก่อน")
        return 1
    before, after = metrics(DIRTY), metrics(CLEAN)
    print("| มิติ | ก่อน | หลัง | วิธีแก้ |")
    print("|------|------|------|--------|")
    print(f"| Completeness (NULL สำคัญ) | {before['null_key']} | {after['null_key']} | dropna / fillna |")
    print(f"| Uniqueness (id ซ้ำ) | {before['dup_id']} | {after['dup_id']} | drop_duplicates |")
    print(f"| Accuracy (outlier อายุ/เดือน) | {before['outlier']} | {after['outlier']} | กรองช่วง |")
    print(f"| Validity (ช่องว่างจังหวัด) | {before['trim']} | {after['trim']} | str.strip |")
    print(f"| จำนวนแถว | {before['rows']} | {after['rows']} | — |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
