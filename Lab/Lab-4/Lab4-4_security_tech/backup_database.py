#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""3-2-1 Backup — สำรองฐานข้อมูล SQLite (บทที่ 4.4)"""

from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = LAB_ROOT / "output" / "backups"


def backup_database(source_db: Path, backup_folder: Path | None = None) -> Path:
    backup_folder = backup_folder or BACKUP_DIR
    backup_folder.mkdir(parents=True, exist_ok=True)
    if not source_db.is_file():
        raise FileNotFoundError(source_db)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = backup_folder / f"{source_db.stem}_backup_{ts}.db"
    shutil.copy2(source_db, dest)
    size_mb = dest.stat().st_size / (1024 * 1024)
    print(f"Backup สำเร็จ: {dest.name} ({size_mb:.2f} MB)")
    return dest


def main() -> int:
    sources = [
        LAB_ROOT / "output" / "school_security.db",
        LAB_ROOT / "output" / "road_accidents.db",
    ]
    done = 0
    for src in sources:
        if src.is_file():
            backup_database(src)
            done += 1
    if not done:
        print("ไม่พบไฟล์ .db — รัน setup_lab.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
