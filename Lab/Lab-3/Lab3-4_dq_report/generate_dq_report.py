#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workshop 3.4 — สร้าง Data Quality Report (HTML)

  python generate_dq_report.py
  python generate_dq_report.py --file ../output/road_accidents_cleaned.csv
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILES = [
    LAB_ROOT / "output" / "road_accidents_cleaned.csv",
    LAB_ROOT / "data" / "dirty_records.csv",
    LAB_ROOT.parent.parent / "data" / "thailand_road_accidents_2568_fix.csv",
]


def find_input(path: Path | None) -> Path:
    if path and path.is_file():
        return path
    for p in DEFAULT_FILES:
        if p.is_file():
            return p
    raise FileNotFoundError("ไม่พบไฟล์ข้อมูล — รัน setup_lab.py และ clean_road_accidents.py")


def generate_report(filepath: Path, output_file: Path) -> None:
    import pandas as pd

    df = pd.read_csv(filepath, encoding="utf-8-sig")
    total_rows = len(df)
    total_cols = len(df.columns)
    null_counts = df.isnull().sum()
    null_pct = (null_counts / total_rows * 100).round(2) if total_rows else null_counts * 0
    dup_count = int(df.duplicated().sum())
    if "accident_id" in df.columns:
        dup_id = total_rows - df["accident_id"].nunique()
        dup_count = max(dup_count, dup_id)
    numeric_stats = df.describe(include="number")

    report_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    dup_class = "error" if dup_count > 0 else "ok"

    html = f"""<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <title>Data Quality Report</title>
  <style>
    body {{ font-family: 'Segoe UI', 'Sarabun', sans-serif; margin: 30px; background: #f5f7fa; }}
    h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
    h2 {{ color: #2980b9; margin-top: 30px; }}
    table {{ border-collapse: collapse; width: 100%; background: white;
             box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin: 15px 0; }}
    th {{ background: #3498db; color: white; padding: 10px 15px; text-align: left; }}
    td {{ padding: 8px 15px; border-bottom: 1px solid #ecf0f1; }}
    tr:hover {{ background: #f0f8ff; }}
    .ok {{ color: green; font-weight: bold; }}
    .warning {{ color: #e67e22; font-weight: bold; }}
    .error {{ color: red; font-weight: bold; }}
    .summary-box {{ background: white; padding: 20px; border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1); display: inline-block;
                    margin: 10px; min-width: 150px; text-align: center; }}
    .summary-number {{ font-size: 2em; font-weight: bold; color: #2980b9; }}
  </style>
</head>
<body>
  <h1>รายงานคุณภาพข้อมูล (Data Quality Report)</h1>
  <p><strong>ไฟล์:</strong> {filepath.name} |
     <strong>วันที่ตรวจ:</strong> {report_date}</p>

  <h2>1. ข้อมูลเบื้องต้น</h2>
  <div>
    <div class="summary-box"><div class="summary-number">{total_rows:,}</div><div>Records</div></div>
    <div class="summary-box"><div class="summary-number">{total_cols}</div><div>Columns</div></div>
    <div class="summary-box"><div class="summary-number {dup_class}">{dup_count}</div><div>แถวซ้ำ</div></div>
    <div class="summary-box"><div class="summary-number">{int(null_counts.sum()):,}</div><div>NULL รวม</div></div>
  </div>

  <h2>2. NULL แต่ละคอลัมน์</h2>
  <table>
    <tr><th>คอลัมน์</th><th>มีค่า</th><th>NULL</th><th>%NULL</th><th>สถานะ</th></tr>
"""

    for col in df.columns:
        n_null = int(null_counts[col])
        pct = float(null_pct[col])
        if pct == 0:
            status, css = "ปกติ", "ok"
        elif pct < 5:
            status, css = "ควรตรวจสอบ", "warning"
        else:
            status, css = "มีปัญหา", "error"
        html += f"""    <tr>
      <td>{col}</td><td>{total_rows - n_null:,}</td><td>{n_null:,}</td>
      <td>{pct}%</td><td class="{css}">{status}</td>
    </tr>\n"""

    html += f"""  </table>

  <h2>3. สถิติตัวเลข</h2>
  {numeric_stats.to_html(border=0, float_format=lambda x: f"{x:,.2f}")}

  <h2>4. สรุป 6 มิติ (แนวทางตรวจ)</h2>
  <table>
    <tr><th>มิติ</th><th>วิธีตรวจใน Lab</th></tr>
    <tr><td>Completeness</td><td>ตาราง NULL ด้านบน</td></tr>
    <tr><td>Uniqueness</td><td>แถวซ้ำ / accident_id</td></tr>
    <tr><td>Accuracy</td><td>min/max ใน describe()</td></tr>
    <tr><td>Validity</td><td>SQL NOT IN, ช่วงเดือน/อายุ</td></tr>
    <tr><td>Consistency</td><td>SQL ตรวจความขัดแย้ง</td></tr>
    <tr><td>Timeliness</td><td>ช่วงวันที่ในข้อมูล</td></tr>
  </table>
</body>
</html>
"""

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html, encoding="utf-8")
    print(f"สร้างรายงาน: {output_file}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=Path, default=None)
    parser.add_argument(
        "--output",
        type=Path,
        default=LAB_ROOT / "output" / "reports" / "dq_report.html",
    )
    args = parser.parse_args()
    try:
        src = find_input(args.file)
        generate_report(src, args.output)
    except FileNotFoundError as e:
        print(e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
