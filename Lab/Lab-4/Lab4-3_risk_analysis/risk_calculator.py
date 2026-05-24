#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""คำนวณคะแนน Risk Matrix — Lab 4.3"""

from __future__ import annotations

import sys

SAMPLE = [
    ("SQL Injection", 2, 5),
    ("รหัสผ่านอ่อนแอ", 4, 5),
    ("ข้อมูล GPS รั่ว", 3, 4),
    ("Server ล่ม", 2, 5),
]


def level(score: int) -> str:
    if score >= 15:
        return "วิกฤต"
    if score >= 10:
        return "สูง"
    if score >= 5:
        return "ปานกลาง"
    return "ต่ำ"


def main() -> int:
    print("| ความเสี่ยง | P | I | คะแนน | ระดับ |")
    print("|-----------|---|---|-------|-------|")
    ranked = []
    for name, p, i in SAMPLE:
        s = p * i
        ranked.append((s, name, p, i))
        print(f"| {name} | {p} | {i} | {s} | {level(s)} |")
    print("\nTop 3 เร่งด่วน:")
    for s, name, _, _ in sorted(ranked, reverse=True)[:3]:
        print(f"  - {name} (คะแนน {s})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
