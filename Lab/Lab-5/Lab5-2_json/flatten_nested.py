#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""แปลง Nested JSON → DataFrame แบน (json_normalize)"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from pandas import json_normalize

LAB_ROOT = Path(__file__).resolve().parents[1]
NESTED = LAB_ROOT / "data" / "sample_nested_accidents.json"


def main() -> None:
    with NESTED.open(encoding="utf-8") as f:
        data = json.load(f)

    df_normal = pd.DataFrame(data)
    print("DataFrame ปกติ (คอลัมน์ สถานที่ เป็น dict):")
    print(df_normal.columns.tolist())

    df_flat = json_normalize(data)
    print("\njson_normalize (แบนแล้ว):")
    print(df_flat)


if __name__ == "__main__":
    main()
