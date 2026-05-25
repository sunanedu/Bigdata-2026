#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mini Project — Dashboard อุบัติเหตุ (Flask + SQLite)"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from flask import Flask, jsonify, render_template, request

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "school_data.db"

app = Flask(__name__)

SELECT_COLS = """
    accident_id, วันที่เกิดเหตุ, เวลาเกิดเหตุ, เดือน,
    จังหวัด, ภูมิภาค, อำเภอ,
    ประเภทถนน, ประเภทยานพาหนะหลัก AS ยานพาหนะหลัก,
    ความรุนแรง, ช่วงเวลากลางวัน_กลางคืน AS ช่วงเวลา,
    จำนวนผู้เสียชีวิต,
    จำนวนผู้บาดเจ็บ AS จำนวนผู้บาดเจ็บรวม
"""


def query_db(sql: str, params: tuple = ()) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def filter_clauses() -> tuple[list[str], list]:
    """เงื่อนไข WHERE จาก query params (Parameterized)"""
    mapping = {
        "province": "จังหวัด",
        "region": "ภูมิภาค",
        "severity": "ความรุนแรง",
        "vehicle": "ประเภทยานพาหนะหลัก",
        "road_type": "ประเภทถนน",
        "time_slot": "ช่วงเวลากลางวัน_กลางคืน",
    }
    parts: list[str] = []
    params: list = []

    for key, col in mapping.items():
        val = request.args.get(key, "").strip()
        if val:
            parts.append(f"{col} = ?")
            params.append(val)

    month = request.args.get("month", "").strip()
    if month.isdigit():
        parts.append("เดือน = ?")
        params.append(int(month))

    return parts, params


def where_sql(parts: list[str]) -> str:
    return (" WHERE " + " AND ".join(parts)) if parts else ""


def parse_filters() -> tuple[str, list]:
    parts, params = filter_clauses()
    return where_sql(parts), params


def parse_limit(default: int = 20, max_limit: int = 500) -> int:
    try:
        n = int(request.args.get("limit", default))
    except ValueError:
        n = default
    return max(1, min(n, max_limit))


def parse_offset() -> int:
    try:
        return max(0, int(request.args.get("offset", 0)))
    except ValueError:
        return 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/meta")
def api_meta():
    """ค่าสำหรับ dropdown filter"""
    def distinct(col: str, limit: int = 200) -> list:
        rows = query_db(
            f"""
            SELECT DISTINCT {col} AS v FROM road_accidents
            WHERE {col} IS NOT NULL AND TRIM({col}) != ''
            ORDER BY v LIMIT ?
            """,
            (limit,),
        )
        return [r["v"] for r in rows]

    return jsonify(
        {
            "provinces": distinct("จังหวัด", 100),
            "regions": distinct("ภูมิภาค", 20),
            "severities": distinct("ความรุนแรง", 20),
            "vehicles": distinct("ประเภทยานพาหนะหลัก", 30),
            "road_types": distinct("ประเภทถนน", 30),
            "time_slots": distinct("ช่วงเวลากลางวัน_กลางคืน", 10),
            "months": [
                {"value": i, "label": m}
                for i, m in enumerate(
                    [
                        "",
                        "ม.ค.",
                        "ก.พ.",
                        "มี.ค.",
                        "เม.ย.",
                        "พ.ค.",
                        "มิ.ย.",
                        "ก.ค.",
                        "ส.ค.",
                        "ก.ย.",
                        "ต.ค.",
                        "พ.ย.",
                        "ธ.ค.",
                    ],
                    start=0,
                )
                if i > 0
            ],
        }
    )


@app.route("/api/summary")
def api_summary():
    where, params = parse_filters()
    rows = query_db(
        f"""
        SELECT
            COUNT(*) AS total_accidents,
            SUM(จำนวนผู้เสียชีวิต) AS total_deaths,
            SUM(จำนวนผู้บาดเจ็บ) AS total_injured,
            ROUND(AVG(จำนวนผู้บาดเจ็บ), 2) AS avg_injured_per_accident,
            COUNT(DISTINCT จังหวัด) AS province_count,
            SUM(CASE WHEN จำนวนผู้เสียชีวิต > 0 THEN 1 ELSE 0 END) AS fatal_cases,
            ROUND(
                100.0 * SUM(CASE WHEN จำนวนผู้เสียชีวิต > 0 THEN 1 ELSE 0 END) / COUNT(*),
                2
            ) AS fatal_rate_pct
        FROM road_accidents
        {where}
        """,
        tuple(params),
    )
    return jsonify(rows[0])


@app.route("/api/by-province")
def api_by_province():
    where, params = parse_filters()
    try:
        limit = int(request.args.get("province_limit", 15))
    except ValueError:
        limit = 15
    limit = max(5, min(limit, 77))
    rows = query_db(
        f"""
        SELECT
            จังหวัด,
            COUNT(*) AS จำนวนครั้ง,
            SUM(จำนวนผู้เสียชีวิต) AS ผู้เสียชีวิต,
            SUM(จำนวนผู้บาดเจ็บ) AS ผู้บาดเจ็บ
        FROM road_accidents
        {where}
        GROUP BY จังหวัด
        ORDER BY จำนวนครั้ง DESC
        LIMIT ?
        """,
        (*params, limit),
    )
    return jsonify(rows)


@app.route("/api/by-region")
def api_by_region():
    where, params = parse_filters()
    rows = query_db(
        f"""
        SELECT
            ภูมิภาค,
            COUNT(*) AS จำนวนครั้ง,
            SUM(จำนวนผู้เสียชีวิต) AS ผู้เสียชีวิต,
            SUM(จำนวนผู้บาดเจ็บ) AS ผู้บาดเจ็บ
        FROM road_accidents
        {where}
        GROUP BY ภูมิภาค
        ORDER BY จำนวนครั้ง DESC
        """,
        tuple(params),
    )
    return jsonify(rows)


@app.route("/api/monthly")
def api_monthly():
    where, params = parse_filters()
    rows = query_db(
        f"""
        SELECT
            เดือน,
            COUNT(*) AS จำนวนครั้ง,
            SUM(จำนวนผู้เสียชีวิต) AS ผู้เสียชีวิต,
            SUM(จำนวนผู้บาดเจ็บ) AS ผู้บาดเจ็บ
        FROM road_accidents
        {where}
        GROUP BY เดือน
        ORDER BY เดือน
        """,
        tuple(params),
    )
    return jsonify(rows)


@app.route("/api/vehicle-type")
def api_vehicle_type():
    where, params = parse_filters()
    limit = parse_limit(12, 20)
    rows = query_db(
        f"""
        SELECT
            ประเภทยานพาหนะหลัก AS ยานพาหนะ,
            COUNT(*) AS จำนวน,
            SUM(จำนวนผู้เสียชีวิต) AS ผู้เสียชีวิต
        FROM road_accidents
        {where}
        GROUP BY ประเภทยานพาหนะหลัก
        ORDER BY จำนวน DESC
        LIMIT ?
        """,
        (*params, limit),
    )
    return jsonify(rows)


@app.route("/api/severity")
def api_severity():
    where, params = parse_filters()
    rows = query_db(
        f"""
        SELECT ความรุนแรง, COUNT(*) AS จำนวน
        FROM road_accidents
        {where}
        GROUP BY ความรุนแรง
        ORDER BY จำนวน DESC
        """,
        tuple(params),
    )
    return jsonify(rows)


@app.route("/api/by-road-type")
def api_by_road_type():
    where, params = parse_filters()
    rows = query_db(
        f"""
        SELECT ประเภทถนน, COUNT(*) AS จำนวน
        FROM road_accidents
        {where}
        GROUP BY ประเภทถนน
        ORDER BY จำนวน DESC
        LIMIT 10
        """,
        tuple(params),
    )
    return jsonify(rows)


@app.route("/api/by-time-slot")
def api_by_time_slot():
    where, params = parse_filters()
    rows = query_db(
        f"""
        SELECT
            ช่วงเวลากลางวัน_กลางคืน AS ช่วงเวลา,
            COUNT(*) AS จำนวน
        FROM road_accidents
        {where}
        GROUP BY ช่วงเวลากลางวัน_กลางคืน
        ORDER BY จำนวน DESC
        """,
        tuple(params),
    )
    return jsonify(rows)


@app.route("/api/accidents")
def api_accidents():
    """ตารางรายละเอียด — รองรับ filter + pagination + ค้นหา"""
    parts, params = filter_clauses()
    q = request.args.get("q", "").strip()
    if q:
        parts.append(
            "(จังหวัด LIKE ? OR อำเภอ LIKE ? OR accident_id LIKE ? "
            "OR ประเภทยานพาหนะหลัก LIKE ? OR ความรุนแรง LIKE ?)"
        )
        like = f"%{q}%"
        params.extend([like, like, like, like, like])

    limit = parse_limit(50, 500)
    offset = parse_offset()
    wsql = where_sql(parts)
    all_params = tuple(params)

    total = query_db(
        f"SELECT COUNT(*) AS n FROM road_accidents {wsql}",
        all_params,
    )[0]["n"]

    rows = query_db(
        f"""
        SELECT {SELECT_COLS.strip()}
        FROM road_accidents
        {wsql}
        ORDER BY วันที่เกิดเหตุ DESC, accident_id DESC
        LIMIT ? OFFSET ?
        """,
        (*all_params, limit, offset),
    )
    return jsonify(
        {
            "total": total,
            "limit": limit,
            "offset": offset,
            "rows": rows,
        }
    )


@app.route("/api/recent")
def api_recent():
    limit = parse_limit(20, 100)
    rows = query_db(
        f"""
        SELECT {SELECT_COLS.strip()}
        FROM road_accidents
        ORDER BY วันที่เกิดเหตุ DESC
        LIMIT ?
        """,
        (limit,),
    )
    return jsonify(rows)


@app.route("/api/search")
def api_search():
    province = request.args.get("province", "").strip()
    if not province:
        return jsonify([])
    rows = query_db(
        f"""
        SELECT {SELECT_COLS.strip()}
        FROM road_accidents
        WHERE จังหวัด = ?
        ORDER BY วันที่เกิดเหตุ DESC
        LIMIT 100
        """,
        (province,),
    )
    return jsonify(rows)


def _port_available(host: str, port: int) -> bool:
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
            return True
        except OSError:
            return False


if __name__ == "__main__":
    import os

    if not DB_PATH.is_file():
        print("ไม่พบ school_data.db — รัน: python ../setup_lab.py")
        raise SystemExit(1)

    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    if not _port_available(host, port):
        print(f"Port {port} ไม่ว่าง — ใช้ 5050")
        port = 5050
    print(f"Dashboard: http://{host}:{port}")
    app.run(debug=True, host=host, port=port, use_reloader=False)
