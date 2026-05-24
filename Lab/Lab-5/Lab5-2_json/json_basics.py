#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lab 5.2 — อ่าน/เขียน JSON พื้นฐาน"""

from __future__ import annotations

import json
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
API_JSON = LAB_ROOT / "data" / "sample_api_data.json"
OUT_JSON = LAB_ROOT / "output" / "output_accidents.json"


def main() -> None:
    with API_JSON.open(encoding="utf-8") as f:
        data = json.load(f)
    print(f"อ่าน {API_JSON.name}: {type(data).__name__}, {len(data)} รายการ")
    print("รายการแรก:", data[0])

    subset = data[:3]
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSON.open("w", encoding="utf-8") as f:
        json.dump(subset, f, ensure_ascii=False, indent=2)
    print(f"บันทึก 3 รายการ → {OUT_JSON}")


if __name__ == "__main__":
    main()
