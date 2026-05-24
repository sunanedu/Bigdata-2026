#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workshop 2.5 — Python Data Pipeline (บทที่ 2.5)
1. ดึงข้อมูลจาก SQLite
2. วิเคราะห์ด้วย Pandas
3. Export เป็น CSV และ JSON
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = LAB_ROOT / "output" / "road_accidents.db"
OUT_DIR = LAB_ROOT / "output" / "exports"


def main() -> int:
  if not DB_PATH.is_file():
    print(f"ไม่พบ {DB_PATH}")
    print("รันก่อน: python setup_lab.py")
    return 1

  try:
    import pandas as pd
  except ImportError:
    print("ติดตั้ง pandas: pip install pandas")
    return 1

  OUT_DIR.mkdir(parents=True, exist_ok=True)
  conn = sqlite3.connect(DB_PATH)
  print("เชื่อมต่อ SQLite สำเร็จ")

  df = pd.read_sql_query("SELECT * FROM road_accidents", conn)
  print(f"ดึงข้อมูล: {df.shape[0]:,} แถว, {df.shape[1]} คอลัมน์")

  deaths = pd.to_numeric(df["จำนวนผู้เสียชีวิต"], errors="coerce").sum()
  injuries = pd.to_numeric(df["จำนวนผู้บาดเจ็บ"], errors="coerce").sum()
  avg_cost = pd.to_numeric(df["ค่าใช้จ่ายรวม_บาท"], errors="coerce").mean()

  print("\nสถิติภาพรวม:")
  print(f"  รวมเสียชีวิต : {int(deaths):,} ราย")
  print(f"  รวมบาดเจ็บ  : {int(injuries):,} ราย")
  print(f"  คชจ เฉลี่ย  : {avg_cost:,.0f} บาท")

  print("\nยานพาหนะที่เกิดเหตุมากที่สุด:")
  print(df["ประเภทยานพาหนะหลัก"].value_counts().head())

  clean_csv = OUT_DIR / "accidents_clean.csv"
  df.to_csv(clean_csv, index=False, encoding="utf-8-sig")
  print(f"\nบันทึก {clean_csv.name}")

  query_province = """
  SELECT
      จังหวัด, ภูมิภาค,
      COUNT(*) AS จำนวนเหตุ,
      SUM(จำนวนผู้เสียชีวิต) AS รวมเสียชีวิต,
      SUM(จำนวนผู้บาดเจ็บ) AS รวมบาดเจ็บ,
      ROUND(SUM(ค่าใช้จ่ายรวม_บาท) / 1000000.0, 2) AS คชจ_รวม_ล้านบาท
  FROM road_accidents
  GROUP BY จังหวัด, ภูมิภาค
  ORDER BY จำนวนเหตุ DESC
  """
  df_province = pd.read_sql_query(query_province, conn)
  conn.close()

  province_csv = OUT_DIR / "province_summary.csv"
  province_json = OUT_DIR / "province_summary.json"
  df_province.to_csv(province_csv, index=False, encoding="utf-8-sig")
  df_province.to_json(
    province_json, orient="records", force_ascii=False, indent=2
  )
  print(f"บันทึก {province_csv.name}")
  print(f"บันทึก {province_json.name}")

  with province_json.open(encoding="utf-8") as f:
    data = json.load(f)
  print(f"\nจำนวนจังหวัดใน JSON: {len(data)}")
  if data:
    print("ตัวอย่างรายการแรก:")
    print(json.dumps(data[0], ensure_ascii=False, indent=2))

  df_num = df.copy()
  df_num["จำนวนผู้เสียชีวิต"] = pd.to_numeric(
    df_num["จำนวนผู้เสียชีวิต"], errors="coerce"
  )
  summary = df_num.groupby("จังหวัด").agg(
    จำนวนเหตุ=("accident_id", "count"),
    รวมเสียชีวิต=("จำนวนผู้เสียชีวิต", "sum"),
  ).reset_index()
  summary_json = OUT_DIR / "summary_by_province.json"
  summary.to_json(summary_json, orient="records", force_ascii=False, indent=2)
  print(f"บันทึก {summary_json.name}")

  print("\nPipeline เสร็จสมบูรณ์")
  return 0


if __name__ == "__main__":
  sys.exit(main())
