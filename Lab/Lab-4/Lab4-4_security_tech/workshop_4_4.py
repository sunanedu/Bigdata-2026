#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Workshop 4.4 — รวมทุกส่วน (Password + SQL Injection + Audit Log + Backup)"""

from __future__ import annotations

import os
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    print("=" * 50)
    print("Lab 4.4 — Security Workshop")
    print("=" * 50)

    print("\n--- ส่วนที่ 1: Password Hash ---")
    from password_hash import demo as hash_demo
    hash_demo()

    print("\n--- ส่วนที่ 2: SQL Injection ---")
    from sql_injection_demo import main as inj_main
    inj_main()

    print("\n--- ส่วนที่ 3: Audit Log ---")
    from audit_log import demo as audit_demo
    audit_demo()

    print("\n--- ส่วนที่ 4: Backup ---")
    from backup_database import main as backup_main
    backup_main()

    print("\nWorkshop 4.4 เสร็จสมบูรณ์")
    return 0


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    sys.exit(main())
