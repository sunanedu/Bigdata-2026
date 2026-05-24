#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workshop 5.4 — Simple Data Pipeline
CSV → Pandas → dashboard_data.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_ROOT.parents[1]
CSV_PATH = REPO_ROOT / "data" / "thailand_road_accidents_2568.csv"
OUT_JSON = LAB_ROOT / "output" / "dashboard_data.json"


def main() -> int:
    try:
        import pandas as pd
    except ImportError:
        print("pip install pandas")
        return 1

    if not CSV_PATH.is_file():
        print(f"ไม่พบ {CSV_PATH}")
        return 1

    print("=== ขั้นที่ 1: อ่าน CSV ===")
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    print(f"จำนวน: {len(df):,} แถว")

    print("\n=== ขั้นที่ 2: กรองปี 2568 ===")
    year_col = "ปี_พ.ศ."
    if year_col not in df.columns:
        print(f"ไม่พบคอลัมน์ {year_col}")
        return 1
    df["ปี_พ.ศ."] = pd.to_numeric(df[year_col], errors="coerce")
    df_2568 = df[df["ปี_พ.ศ."] == 2568].copy()
    print(f"ปี 2568: {len(df_2568):,} แถว")

    print("\n=== ขั้นที่ 3: สรุปตามยานพาหนะ ===")
    vehicle_col = "ประเภทยานพาหนะหลัก"
    injury_col = "จำนวนผู้บาดเจ็บ"
    if vehicle_col not in df_2568.columns:
        print(f"ไม่พบคอลัมน์ {vehicle_col}")
        return 1
    df_2568[injury_col] = pd.to_numeric(df_2568[injury_col], errors="coerce").fillna(0)

    summary = (
        df_2568.groupby(vehicle_col)[injury_col]
        .agg(จำนวนอุบัติเหตุ="count", ผู้บาดเจ็บรวม="sum")
        .reset_index()
        .rename(columns={vehicle_col: "ยานพาหนะ"})
        .sort_values("ผู้บาดเจ็บรวม", ascending=False)
        .head(10)
    )
    print(summary)

    print("\n=== ขั้นที่ 4: บันทึก JSON ===")
    payload = {
        "title": "สรุปอุบัติเหตุปี 2568 ตามยานพาหนะ",
        "source": str(CSV_PATH.name),
        "records_filtered": int(len(df_2568)),
        "top_vehicles": summary.to_dict(orient="records"),
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"บันทึก → {OUT_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
