#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mini Project — Dashboard อุบัติเหตุทางถนน ปี 2568
Backend: Flask + SQLite (school_data.db)
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "school_data.db"

app = Flask(__name__)


def query_db(sql: str, params: tuple = ()) -> list[dict]:
    """รัน SQL แบบ Parameterized Query — ปลอดภัยจาก SQL Injection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/summary")
def api_summary():
    rows = query_db(
        """
        SELECT
            COUNT(*) AS total_accidents,
            SUM(จำนวนผู้เสียชีวิต) AS total_deaths,
            SUM(จำนวนผู้บาดเจ็บ) AS total_injured,
            ROUND(AVG(จำนวนผู้บาดเจ็บ), 2) AS avg_injured_per_accident
        FROM road_accidents
        """
    )
    return jsonify(rows[0])


@app.route("/api/by-province")
def api_by_province():
    rows = query_db(
        """
        SELECT
            จังหวัด,
            COUNT(*) AS จำนวนครั้ง,
            SUM(จำนวนผู้เสียชีวิต) AS ผู้เสียชีวิต,
            SUM(จำนวนผู้บาดเจ็บ) AS ผู้บาดเจ็บ
        FROM road_accidents
        GROUP BY จังหวัด
        ORDER BY จำนวนครั้ง DESC
        LIMIT 10
        """
    )
    return jsonify(rows)


@app.route("/api/monthly")
def api_monthly():
    rows = query_db(
        """
        SELECT
            เดือน,
            COUNT(*) AS จำนวนครั้ง,
            SUM(จำนวนผู้เสียชีวิต) AS ผู้เสียชีวิต
        FROM road_accidents
        GROUP BY เดือน
        ORDER BY เดือน
        """
    )
    return jsonify(rows)


@app.route("/api/vehicle-type")
def api_vehicle_type():
    rows = query_db(
        """
        SELECT
            ประเภทยานพาหนะหลัก AS ยานพาหนะ,
            COUNT(*) AS จำนวน
        FROM road_accidents
        GROUP BY ประเภทยานพาหนะหลัก
        ORDER BY จำนวน DESC
        """
    )
    return jsonify(rows)


@app.route("/api/severity")
def api_severity():
    rows = query_db(
        """
        SELECT
            ความรุนแรง,
            COUNT(*) AS จำนวน
        FROM road_accidents
        GROUP BY ความรุนแรง
        ORDER BY จำนวน DESC
        """
    )
    return jsonify(rows)


@app.route("/api/recent")
def api_recent():
    rows = query_db(
        """
        SELECT
            accident_id,
            วันที่เกิดเหตุ,
            จังหวัด,
            ภูมิภาค,
            ประเภทยานพาหนะหลัก AS ยานพาหนะหลัก,
            ความรุนแรง,
            จำนวนผู้เสียชีวิต,
            จำนวนผู้บาดเจ็บ AS จำนวนผู้บาดเจ็บรวม
        FROM road_accidents
        ORDER BY วันที่เกิดเหตุ DESC
        LIMIT 20
        """
    )
    return jsonify(rows)


@app.route("/api/search")
def api_search():
    province = request.args.get("province", "").strip()
    if not province:
        return jsonify([])
    rows = query_db(
        """
        SELECT accident_id, วันที่เกิดเหตุ, จังหวัด,
               ประเภทยานพาหนะหลัก AS ยานพาหนะหลัก, ความรุนแรง,
               จำนวนผู้เสียชีวิต, จำนวนผู้บาดเจ็บ AS จำนวนผู้บาดเจ็บรวม
        FROM road_accidents
        WHERE จังหวัด = ?
        ORDER BY วันที่เกิดเหตุ DESC
        LIMIT 50
        """,
        (province,),
    )
    return jsonify(rows)


@app.route("/api/by-region")
def api_by_region():
    region = request.args.get("region", "").strip()
    if region:
        rows = query_db(
            """
            SELECT accident_id, วันที่เกิดเหตุ, จังหวัด, ภูมิภาค,
                   ประเภทยานพาหนะหลัก AS ยานพาหนะหลัก, ความรุนแรง,
                   จำนวนผู้เสียชีวิต, จำนวนผู้บาดเจ็บ AS จำนวนผู้บาดเจ็บรวม
            FROM road_accidents
            WHERE ภูมิภาค = ?
            ORDER BY วันที่เกิดเหตุ DESC
            LIMIT 50
            """,
            (region,),
        )
    else:
        rows = query_db(
            """
            SELECT accident_id, วันที่เกิดเหตุ, จังหวัด, ภูมิภาค,
                   ประเภทยานพาหนะหลัก AS ยานพาหนะหลัก, ความรุนแรง,
                   จำนวนผู้เสียชีวิต, จำนวนผู้บาดเจ็บ AS จำนวนผู้บาดเจ็บรวม
            FROM road_accidents
            ORDER BY วันที่เกิดเหตุ DESC
            LIMIT 50
            """
        )
    return jsonify(rows)


if __name__ == "__main__":
    if not DB_PATH.is_file():
        print("ไม่พบ school_data.db — รัน: python ../setup_lab.py")
        raise SystemExit(1)
    print("Dashboard: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
