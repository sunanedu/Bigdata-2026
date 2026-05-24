#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""นำเข้า sample_api_data.json → MongoDB หรือโหมดออฟไลน์"""

from __future__ import annotations

import json
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
API_JSON = LAB_ROOT / "data" / "sample_api_data.json"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from collection_store import JsonCollection  # noqa: E402
from products_crud import use_mongodb  # noqa: E402


def main() -> int:
    if not API_JSON.is_file():
        print("รัน python setup_lab.py ก่อน")
        return 1

    with API_JSON.open(encoding="utf-8") as f:
        records = json.load(f)

    if use_mongodb():
        from pymongo import MongoClient

        client = MongoClient("mongodb://localhost:27017/")
        col = client["school_db"]["accidents"]
        col.delete_many({})
        col.insert_many(records)
        print(f"MongoDB accidents: {col.count_documents({})} รายการ")
    else:
        col = JsonCollection("accidents")
        col.path.write_text("[]", encoding="utf-8")
        for r in records:
            col.insert_one(dict(r))
        print(f"ออฟไลน์ accidents: {len(col.find())} รายการ → {col.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
