#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workshop 5.3 — MongoDB CRUD (products)
ถ้าไม่มี MongoDB จะใช้ JsonCollection อัตโนมัติ
"""

from __future__ import annotations

import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from collection_store import JsonCollection  # noqa: E402

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "school_db"
COLLECTION = "products"


def use_mongodb() -> bool:
    try:
        from pymongo import MongoClient  # noqa: F401
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        return True
    except Exception:
        return False


def run_crud_mongo() -> None:
    from pymongo import MongoClient

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    col = db[COLLECTION]
    col.delete_many({})

    print("=== INSERT ===")
    col.insert_many(
        [
            {"name": "สมุด", "price": 25, "stock": 100},
            {"name": "ดินสอ", "price": 10, "stock": 200},
            {"name": "ยางลบ", "price": 5, "stock": 150},
        ]
    )
    print(f"จำนวน: {col.count_documents({})}")

    print("\n=== FIND ===")
    for doc in col.find({"price": {"$lt": 20}}):
        print(doc)

    print("\n=== UPDATE ===")
    col.update_one({"name": "สมุด"}, {"$set": {"price": 30}})
    print(col.find_one({"name": "สมุด"}))

    print("\n=== DELETE ===")
    col.delete_one({"name": "ยางลบ"})
    print(f"เหลือ: {col.count_documents({})}")


def run_crud_offline() -> None:
    col = JsonCollection(COLLECTION)
    col.path.write_text("[]", encoding="utf-8")

    print("=== โหมดออฟไลน์ (JSON file) ===\n=== INSERT ===")
    for item in [
        {"name": "สมุด", "price": 25, "stock": 100},
        {"name": "ดินสอ", "price": 10, "stock": 200},
        {"name": "ยางลบ", "price": 5, "stock": 150},
    ]:
        col.insert_one(item)
    print(f"จำนวน: {len(col.find())}")

    print("\n=== FIND (price < 20) ===")
    for doc in col.find():
        if doc.get("price", 0) < 20:
            print(doc)

    print("\n=== UPDATE ===")
    col.update_one({"name": "สมุด"}, {"price": 30})
    print(col.find({"name": "สมุด"}))

    print("\n=== DELETE ===")
    col.delete_one({"name": "ยางลบ"})
    print(f"เหลือ: {len(col.find())}")
    print(f"ไฟล์: {col.path}")


def main() -> int:
    if use_mongodb():
        print("เชื่อมต่อ MongoDB สำเร็จ\n")
        run_crud_mongo()
    else:
        print("ไม่พบ MongoDB — ใช้โหมดออฟไลน์\n")
        run_crud_offline()
    return 0


if __name__ == "__main__":
    sys.exit(main())
