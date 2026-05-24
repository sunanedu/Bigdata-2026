#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hash Password ด้วย SHA-256 + Salt (บทที่ 4.4)"""

from __future__ import annotations

import hashlib
import os


def hash_password_with_salt(password: str) -> tuple[str, str]:
    salt = os.urandom(16)
    salted = salt + password.encode("utf-8")
    hashed = hashlib.sha256(salted).hexdigest()
    return salt.hex(), hashed


def verify_password(password: str, salt_hex: str, stored_hash: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    salted = salt + password.encode("utf-8")
    return hashlib.sha256(salted).hexdigest() == stored_hash


def demo() -> None:
    password = "SomchaiPass2026"
    salt, hashed = hash_password_with_salt(password)
    print("เก็บในฐานข้อมูล:")
    print(f"  Salt: {salt[:32]}...")
    print(f"  Hash: {hashed[:32]}...")
    ok = verify_password("SomchaiPass2026", salt, hashed)
    bad = verify_password("WrongPassword", salt, hashed)
    print(f"\nLogin ถูก: {'สำเร็จ' if ok else 'ล้มเหลว'}")
    print(f"Login ผิด: {'สำเร็จ' if bad else 'ล้มเหลว'}")


if __name__ == "__main__":
    demo()
