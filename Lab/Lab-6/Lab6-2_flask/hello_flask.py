#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lab 6.2 — Flask Hello World (ก่อนทำ Mini Project)"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello! Dashboard พร้อมใช้งาน! ไปที่ Lab6-mini_project/app.py สำหรับโปรเจกต์เต็ม"


if __name__ == "__main__":
    print("เปิด http://127.0.0.1:5001")
    app.run(debug=True, port=5001)
