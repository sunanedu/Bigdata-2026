#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ทดสอบ API โดยไม่ต้องเปิดเบราว์เซอร์ (Flask test client)"""

from __future__ import annotations

import sys
from pathlib import Path

MINI = Path(__file__).resolve().parents[1] / "Lab6-mini_project"
sys.path.insert(0, str(MINI))

from app import app  # noqa: E402


def main() -> int:
    if not (MINI / "school_data.db").is_file():
        print("รัน python setup_lab.py ก่อน")
        return 1

    client = app.test_client()
    endpoints = [
        "/api/meta",
        "/api/summary",
        "/api/by-province",
        "/api/by-region",
        "/api/monthly",
        "/api/vehicle-type",
        "/api/severity",
        "/api/by-road-type",
        "/api/by-time-slot",
        "/api/accidents?limit=10",
        "/api/search?province=เชียงใหม่",
    ]
    print("ทดสอบ API:\n")
    for path in endpoints:
        resp = client.get(path)
        ok = "OK" if resp.status_code == 200 else "FAIL"
        print(f"  [{ok}] {path} — status {resp.status_code}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
