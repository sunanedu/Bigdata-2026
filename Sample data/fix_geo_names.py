#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
แก้ชื่อ จังหวัด อำเภอ ตำบล ใน thailand_road_accidents_2568.csv
โดยอ้างอิงพิกัด (ละติจูด, ลองจิจูด) กับ source-data.csv

ผลลัพธ์: thailand_road_accidents_2568_fix.csv
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

try:
    from scipy.spatial import cKDTree
except ImportError:
    cKDTree = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = Path(__file__).resolve().parent
INPUT_CSV = SAMPLE / "thailand_road_accidents_2568.csv"
REF_CSV = ROOT / "ฐานข้อมูล ชื่อจังหวัด-อำเภอ-ตำบล" / "source-data.csv"
OUTPUT_CSV = SAMPLE / "thailand_road_accidents_2568_fix.csv"
REPORT_CSV = SAMPLE / "geo_fix_report.csv"


def norm_province(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = re.sub(r"^จ\.?\s+", "", s)
    s = re.sub(r"^จังหวัด\s+", "", s)
    return s.strip()


def norm_amphoe(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = re.sub(r"^อ\.?\s+", "", s)
    s = re.sub(r"^อำเภอ\s+", "", s)
    return s.strip()


def norm_tambon(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = re.sub(r"^ต\.?\s+", "", s)
    s = re.sub(r"^ตำบล\s+", "", s)
    return s.strip()


def region_from_province_code(code: int) -> str:
    """แบ่งภูมิภาคจากรหัสจังหวัด (มาตรฐานกรมการปกครอง)"""
    if code >= 80:
        return "ภาคใต้"
    if 50 <= code <= 58:
        return "ภาคเหนือ"
    if 30 <= code <= 49:
        return "ภาคตะวันออกเฉียงเหนือ"
    if 20 <= code <= 27:
        return "ภาคตะวันออก"
    if 10 <= code <= 19 or 60 <= code <= 67 or 70 <= code <= 76:
        return "ภาคกลาง"
    return "ภาคกลาง"


def build_reference(ref: pd.DataFrame) -> pd.DataFrame:
    ref = ref.copy()
    ref["prov"] = ref["CHANGWAT_T"].map(norm_province)
    ref["amp"] = ref["AMPHOE_T"].map(norm_amphoe)
    ref["tambon"] = ref["TAMBON_T"].map(norm_tambon)
    ref["prov_code"] = pd.to_numeric(ref["CH_ID"], errors="coerce").astype("Int64")

    agg = (
        ref.groupby("TA_ID", as_index=False)
        .agg(
            lat=("LAT", "mean"),
            lon=("LONG", "mean"),
            prov=("prov", "first"),
            amp=("amp", "first"),
            tambon=("tambon", "first"),
            prov_code=("prov_code", "first"),
        )
    )
    return agg.dropna(subset=["lat", "lon"])


def nearest_lookup(
    lat: pd.Series, lon: pd.Series, ref_pts: pd.DataFrame
) -> pd.DataFrame:
    coords = ref_pts[["lat", "lon"]].to_numpy()
    query = pd.DataFrame({"lat": lat, "lon": lon}).to_numpy()

    if cKDTree is not None:
        tree = cKDTree(coords)
        dist, idx = tree.query(query, k=1)
    else:
        # fallback ช้ากว่า แต่ไม่ต้องมี scipy
        import numpy as np

        dist = np.empty(len(query))
        idx = np.empty(len(query), dtype=int)
        for i, (la, lo) in enumerate(query):
            d = (coords[:, 0] - la) ** 2 + (coords[:, 1] - lo) ** 2
            j = int(d.argmin())
            dist[i], idx[i] = d[j] ** 0.5, j

    out = ref_pts.iloc[idx].reset_index(drop=True)
    out["geo_match_km"] = dist * 111.0  # ประมาณ km
    return out


def main() -> None:
    if not INPUT_CSV.is_file():
        raise FileNotFoundError(f"ไม่พบ {INPUT_CSV}")
    if not REF_CSV.is_file():
        raise FileNotFoundError(f"ไม่พบ {REF_CSV}")

    acc = pd.read_csv(INPUT_CSV, encoding="utf-8-sig")
    ref_raw = pd.read_csv(REF_CSV, encoding="utf-8-sig")
    ref_pts = build_reference(ref_raw)

    matched = nearest_lookup(acc["ละติจูด"], acc["ลองจิจูด"], ref_pts)

    old_prov = acc["จังหวัด"].astype(str)
    old_amp = acc["อำเภอ"].astype(str)
    old_region = acc["ภูมิภาค"].astype(str)

    acc["จังหวัด"] = matched["prov"]
    acc["อำเภอ"] = matched["amp"]
    acc["ตำบล"] = matched["tambon"]
    acc["ภูมิภาค"] = matched["prov_code"].map(
        lambda c: region_from_province_code(int(c)) if pd.notna(c) else "ภาคกลาง"
    )
    acc["geo_match_km"] = matched["geo_match_km"].round(3)

    # ใส่คอลัมน์ ตำบล หลัง อำเภอ
    cols = list(acc.columns)
    if "ตำบล" in cols:
        cols.remove("ตำบล")
        amp_i = cols.index("อำเภอ")
        cols.insert(amp_i + 1, "ตำบล")
        acc = acc[cols]

    changed = (old_prov != acc["จังหวัด"]) | (old_amp != acc["อำเภอ"])
    report = pd.DataFrame(
        {
            "accident_id": acc["accident_id"],
            "จังหวัด_เดิม": old_prov,
            "อำเภอ_เดิม": old_amp,
            "ภูมิภาค_เดิม": old_region,
            "จังหวัด_ใหม่": acc["จังหวัด"],
            "อำเภอ_ใหม่": acc["อำเภอ"],
            "ตำบล_ใหม่": acc["ตำบล"],
            "ภูมิภาค_ใหม่": acc["ภูมิภาค"],
            "geo_match_km": acc["geo_match_km"],
            "เปลี่ยนแปลง": changed,
        }
    )
    report[report["เปลี่ยนแปลง"]].to_csv(REPORT_CSV, index=False, encoding="utf-8-sig")

    # ลบคอลัมน์ช่วยก่อนบันทึก (เก็บได้ถ้าต้องการตรวจสอบ)
    out = acc.drop(columns=["geo_match_km"], errors="ignore")
    out.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    # ตรวจสอบความถูกต้องหลังแก้
    ref_pairs = ref_pts[["prov", "amp"]].drop_duplicates()
    check = out[["จังหวัด", "อำเภอ"]].rename(
        columns={"จังหวัด": "prov", "อำเภอ": "amp"}
    )
    m = check.merge(ref_pairs, on=["prov", "amp"], how="left", indicator=True)
    valid_rate = (m["_merge"] == "both").mean()

    print("แก้ไขข้อมูลภูมิศาสลร์เสร็จ")
    print(f"  อ่าน: {INPUT_CSV.name} ({len(acc):,} แถว)")
    print(f"  อ้างอิง: {REF_CSV.name} ({len(ref_pts):,} ตำบล)")
    print(f"  บันทึก: {OUTPUT_CSV.name}")
    print(f"  รายงานการเปลี่ยน: {REPORT_CSV.name} ({changed.sum():,} แถว)")
    print(f"  จับคู่ จังหวัด+อำเภอ ถูกต้องหลังแก้: {valid_rate:.1%}")
    print(f"  ระยะจับคูพิกัดเฉลี่ย: {acc['geo_match_km'].mean():.2f} km")


if __name__ == "__main__":
    main()
