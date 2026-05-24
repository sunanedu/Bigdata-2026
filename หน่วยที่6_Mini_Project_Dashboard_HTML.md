# หน่วยที่ 6: Mini Project — Dashboard ข้อมูลด้วย HTML
### วิชา: การจัดการข้อมูลขนาดใหญ่เบื้องต้น | Introduction to Big Data (พ.ศ. 2026)
**เวลาเรียน: 18 ชั่วโมง** | **เครื่องมือหลัก:** Python Flask, HTML, CSS, JavaScript, Chart.js, SQLite

---

## จุดประสงค์การเรียนรู้

เมื่อเรียนจบหน่วยนี้ นักเรียนจะสามารถ:

1. อธิบายสถาปัตยกรรม Dashboard แบบ Backend → API → Frontend ได้
2. เลือกประเภทกราฟให้เหมาะกับข้อมูลที่ต้องการนำเสนอได้
3. สร้าง Flask API Endpoint ที่ดึงข้อมูลจาก SQLite และส่งเป็น JSON ได้
4. เขียน HTML + JavaScript ดึงข้อมูลจาก API ด้วย `fetch()` และแสดงผลด้วย Chart.js ได้
5. เพิ่มฟีเจอร์ Filter, Search และ Export CSV ลงใน Dashboard ได้
6. นำเสนอ Mini Project อธิบายที่มาของข้อมูล, SQL, คุณภาพ, และความปลอดภัยได้

> **ข้อมูลที่ใช้ตลอดหน่วยนี้:**
> ฐานข้อมูล `school_data.db` (SQLite) และ
> ข้อมูลอุบัติเหตุ `thailand_road_accidents_2568.csv` ที่เตรียมไว้ตลอดหลักสูตร
> ไฟล์ template: `app_template.py` และ `index_template.html` จากแฟลชไดร์ฟครู

---

## โครงสร้างโปรเจกต์ (ภาพรวม)

```
📁 my_bigdata_project/
├── 📄 README.md              ← อธิบายโปรเจกต์
├── 📄 app.py                 ← Python Flask Backend (สมองของระบบ)
├── 📄 school_data.db         ← SQLite Database (คลังข้อมูล)
├── 📁 static/
│   ├── 📄 style.css          ← ตกแต่งหน้าเว็บ
│   └── 📄 chart.min.js       ← Chart.js (ดาวน์โหลดไว้ล่วงหน้า — ออฟไลน์)
└── 📁 templates/
    └── 📄 index.html         ← Dashboard หน้าหลัก (หน้าตาของระบบ)
```

---

# บทที่ 6.1 — สถาปัตยกรรมของ Dashboard
**(2 ชั่วโมง)**

---

## 🏛️ Dashboard คืออะไร? ทำงานอย่างไร?

**Dashboard** (แดชบอร์ด) คือหน้าจอแสดงผลข้อมูลสำคัญในรูปแบบภาพ (กราฟ, ตาราง, ตัวเลขสรุป) ที่ช่วยให้ผู้ใช้เข้าใจภาพรวมได้ในชั่วพริบตา

> **เปรียบเทียบ:** Dashboard ของรถยนต์ — มองแวบเดียวรู้ทันทีว่าน้ำมันเหลือเท่าไร ความเร็วเท่าไร อุณหภูมิเครื่องยนต์เป็นอย่างไร ไม่ต้องเปิดฝากระโปรงรถทุกครั้ง

**ตัวอย่าง Dashboard ในชีวิตจริง:**

```
🏥 โรงพยาบาล   → Dashboard แสดงจำนวนผู้ป่วย, เตียงว่าง, ยาใกล้หมด
🏫 โรงเรียน    → Dashboard แสดงคะแนนเฉลี่ย, อัตราการขาดเรียน, วิชาที่ตก
🚗 กรมทางหลวง  → Dashboard แสดงจุดอุบัติเหตุ, ช่วงเวลาเสี่ยง, จังหวัดอันตราย
🏪 ร้านสะดวกซื้อ → Dashboard แสดงยอดขาย, สินค้าขาดสต็อก, ชั่วโมงพีค
```

---

## 🏗️ สถาปัตยกรรม 3 ชั้น (3-Tier Architecture)

**สถาปัตยกรรม** (อาร์คิเทคเจอร์) = โครงสร้างการทำงานของระบบ

```
ชั้นที่ 1: DATA LAYER (เดต้า เลเยอร์)
          "ชั้นข้อมูล"
┌─────────────────────────┐
│  school_data.db         │
│  (SQLite Database)      │  ← เก็บข้อมูลดิบทั้งหมด
│                         │
│  ตาราง: students        │
│  ตาราง: road_accidents  │
│  ตาราง: scores          │
└────────────┬────────────┘
             │ SQL Query
             ▼
ชั้นที่ 2: BACKEND LAYER (แบ็กเอนด์ เลเยอร์)
           "ชั้นประมวลผล"
┌─────────────────────────┐
│  app.py                 │
│  (Python Flask)         │  ← รับคำขอ, Query DB, ส่ง JSON
│                         │
│  /api/summary           │
│  /api/accidents         │
│  /api/by-province       │
└────────────┬────────────┘
             │ JSON Response
             ▼
ชั้นที่ 3: FRONTEND LAYER (ฟรอนต์เอนด์ เลเยอร์)
            "ชั้นแสดงผล"
┌─────────────────────────┐
│  index.html             │
│  (HTML + CSS + JS)      │  ← แสดงกราฟและตารางให้ผู้ใช้เห็น
│                         │
│  Chart.js → กราฟ        │
│  fetch() → ดึงข้อมูล    │
│  CSS     → ตกแต่ง       │
└─────────────────────────┘
```

**การทำงานเมื่อผู้ใช้เปิด Dashboard:**

```
1. ผู้ใช้เปิดเบราว์เซอร์ → ไปที่ http://localhost:5000
2. Flask ส่งไฟล์ index.html ให้เบราว์เซอร์
3. JavaScript ใน index.html เรียก fetch('/api/summary')
4. Flask รับคำขอ → Query SQLite → ได้ข้อมูล
5. Flask แปลงเป็น JSON → ส่งกลับให้ JavaScript
6. JavaScript รับ JSON → วาดกราฟด้วย Chart.js
7. ผู้ใช้เห็นกราฟบนหน้าเว็บ! ✅
```

---

## 📊 หลักการ Data Visualization — กราฟอะไรใช้เมื่อไหร่?

**Data Visualization** (เดต้า วิชวลไลเซชัน) = การแปลงข้อมูลเป็นภาพที่เข้าใจง่าย

> **กฎทอง:** เลือกกราฟตามคำถามที่ต้องการตอบ ไม่ใช่ตามความสวยงาม

### ตารางเลือกประเภทกราฟ

| คำถามที่ต้องการตอบ | กราฟที่เหมาะสม | ตัวอย่าง |
|-------------------|--------------|---------|
| เปรียบเทียบปริมาณระหว่างหมวดหมู่ | **Bar Chart** (บาร์ ชาร์ต) | อุบัติเหตุแต่ละจังหวัด |
| แสดงแนวโน้มตามเวลา | **Line Chart** (ไลน์ ชาร์ต) | อุบัติเหตุรายเดือน |
| แสดงสัดส่วน/เปอร์เซ็นต์ | **Pie Chart** (พาย ชาร์ต) | สัดส่วนยานพาหนะ |
| แสดงสัดส่วนที่อ่านง่ายกว่า Pie | **Doughnut Chart** (โดนัท ชาร์ต) | สัดส่วนความรุนแรง |
| เปรียบเทียบหลายตัวแปรพร้อมกัน | **Radar Chart** (เรดาร์ ชาร์ต) | ประสิทธิภาพรายด้าน |
| แสดงข้อมูลรายละเอียดหลายคอลัมน์ | **ตาราง (Table)** | รายชื่ออุบัติเหตุ |

### ตัวอย่างการเลือกกราฟสำหรับ Dashboard อุบัติเหตุ

```
Dashboard อุบัติเหตุทางถนน ปี 2568:

📊 Bar Chart   → "10 จังหวัดที่มีอุบัติเหตุมากที่สุด"
                 เปรียบเทียบจำนวนระหว่างจังหวัด

📈 Line Chart  → "แนวโน้มอุบัติเหตุรายเดือน ม.ค.–ธ.ค."
                 เห็นว่าเดือนไหนพีค เดือนไหนลด

🥧 Pie Chart   → "สัดส่วนยานพาหนะที่เกิดอุบัติเหตุ"
                 มอเตอร์ไซค์ 72%, รถยนต์ 18%, อื่นๆ 10%

🍩 Doughnut   → "ระดับความรุนแรง"
                 เสียชีวิต / บาดเจ็บสาหัส / บาดเจ็บเล็กน้อย

📋 ตาราง      → "รายการอุบัติเหตุล่าสุด 20 รายการ"
                 รายละเอียดที่ต้องการความแม่นยำ
```

---

## 🖼️ Workshop 6.1 — วาด Wireframe Dashboard

**Wireframe** (ไวร์เฟรม) = ภาพร่างหน้าจอ แสดงตำแหน่งของ element ต่างๆ ก่อนลงมือเขียนโค้ด เหมือนพิมพ์เขียวก่อนสร้างบ้าน

```
┌──────────────────────────────────────────────────────────┐
│  🚗 Dashboard อุบัติเหตุทางถนน ประเทศไทย ปี 2568        │
├──────────────────────────────────────────────────────────┤
│  [📦 20,000 ครั้ง]  [💀 471 ราย]  [🤕 20,573 ราย]       │
│  "อุบัติเหตุรวม"   "เสียชีวิต"    "บาดเจ็บ"              │
├─────────────────────────┬────────────────────────────────┤
│                         │                                │
│   Bar Chart             │   Pie Chart                    │
│   "Top 10 จังหวัด"      │   "สัดส่วนยานพาหนะ"           │
│                         │                                │
├─────────────────────────┴────────────────────────────────┤
│                                                          │
│   Line Chart — "แนวโน้มอุบัติเหตุรายเดือน"               │
│                                                          │
├──────────────────────────────────────────────────────────┤
│   [🔍 ค้นหา...]  [📥 Export CSV]                         │
│   ตารางข้อมูลรายละเอียด                                  │
│   accident_id | วันที่ | จังหวัด | ความรุนแรง | ยานพาหนะ │
└──────────────────────────────────────────────────────────┘
```

**งานในห้องเรียน:** วาด Wireframe บนกระดาษ A4 โดยกำหนด:
1. หัวข้อ Dashboard คืออะไร?
2. จะแสดง KPI Card (ตัวเลขสรุป) อะไรบ้าง?
3. จะใช้กราฟประเภทไหน ตรงไหน?
4. ตารางข้อมูลแสดงคอลัมน์อะไรบ้าง?

---

# บทที่ 6.2 — สร้าง Backend ด้วย Python Flask
**(4 ชั่วโมง)**

---

## 🐍 Flask คืออะไร?

**Flask** (แฟลสก์) คือ Web Framework (เว็บ เฟรมเวิร์ก) ขนาดเล็กของ Python ที่ช่วยให้เราสร้างเว็บแอปและ API ได้ง่ายๆ โดยไม่ต้องตั้งค่าซับซ้อน

> **เปรียบเทียบ:** Flask เหมือนเคาน์เตอร์บริการ — ลูกค้า (Browser) มาขอข้อมูล พนักงาน (Flask) วิ่งไปหยิบของ (SQLite) มาส่งให้

**API** (เอพีไอ) = Application Programming Interface = ช่องทางที่โปรแกรมต่างๆ ใช้คุยกัน ในที่นี้คือ URL ที่ Browser เรียกเพื่อขอข้อมูล

---

## ⚙️ ติดตั้ง Flask (จากแฟลชไดร์ฟ — ออฟไลน์)

```bash
# เปิด Terminal / Command Prompt แล้วพิมพ์:
pip install flask --find-links /path/to/flashdrive/python_packages --no-index

# ตรวจสอบว่าติดตั้งสำเร็จ:
python -c "import flask; print(flask.__version__)"
```

---

## 🚀 Flask เบื้องต้น — Hello World

```python
# app.py — ไฟล์หลักของ Backend

from flask import Flask

app = Flask(__name__)   # ← สร้าง Flask Application

# กำหนด Route (เส้นทาง URL)
@app.route('/')         # ← เมื่อเข้า http://localhost:5000/
def home():
    return 'Hello! Dashboard พร้อมใช้งาน!'

if __name__ == '__main__':
    app.run(debug=True)  # ← เริ่มรัน Server ที่ port 5000
```

**รันด้วยคำสั่ง:**
```bash
python app.py
```

**ผลลัพธ์ใน Terminal:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

เปิดเบราว์เซอร์ไปที่ `http://localhost:5000` → เห็นข้อความ "Hello! Dashboard พร้อมใช้งาน!"

---

## 🔌 สร้าง API Endpoint ที่ดึงข้อมูลจาก SQLite

**Endpoint** (เอนด์พอยท์) = URL แต่ละจุดที่ให้บริการข้อมูลต่างๆ

```python
# app.py — ฉบับสมบูรณ์สำหรับ Dashboard อุบัติเหตุ

from flask import Flask, jsonify, render_template
import sqlite3
import pandas as pd

app = Flask(__name__)

DB_PATH = 'school_data.db'   # ← path ของ SQLite database

# ======== ฟังก์ชันช่วย: เชื่อมต่อ DB และ Query ========
def query_db(sql, params=()):
    """
    รัน SQL Query แล้วคืนค่าเป็น list of dict
    ปลอดภัยจาก SQL Injection ด้วย Parameterized Query
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # ← ทำให้ผลลัพธ์เป็น dict แทน tuple
    cursor = conn.cursor()
    cursor.execute(sql, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


# ======== Route หลัก: ส่งไฟล์ HTML ========
@app.route('/')
def index():
    return render_template('index.html')


# ======== Endpoint 1: สรุปข้อมูลรวม ========
@app.route('/api/summary')
def api_summary():
    """
    GET /api/summary
    คืนค่า: ตัวเลขสรุปภาพรวม (KPI Cards)
    """
    rows = query_db("""
        SELECT
            COUNT(*)                           AS total_accidents,
            SUM(จำนวนผู้เสียชีวิต)              AS total_deaths,
            SUM(จำนวนผู้บาดเจ็บรวม)            AS total_injured,
            ROUND(AVG(จำนวนผู้บาดเจ็บรวม), 2)  AS avg_injured_per_accident
        FROM road_accidents
    """)
    return jsonify(rows[0])


# ======== Endpoint 2: อุบัติเหตุ Top 10 จังหวัด ========
@app.route('/api/by-province')
def api_by_province():
    """
    GET /api/by-province
    คืนค่า: จำนวนอุบัติเหตุของแต่ละจังหวัด เรียงมากไปน้อย Top 10
    """
    rows = query_db("""
        SELECT
            จังหวัด,
            COUNT(*)                AS จำนวนครั้ง,
            SUM(จำนวนผู้เสียชีวิต)  AS ผู้เสียชีวิต,
            SUM(จำนวนผู้บาดเจ็บรวม) AS ผู้บาดเจ็บ
        FROM road_accidents
        GROUP BY จังหวัด
        ORDER BY จำนวนครั้ง DESC
        LIMIT 10
    """)
    return jsonify(rows)


# ======== Endpoint 3: แนวโน้มรายเดือน ========
@app.route('/api/monthly')
def api_monthly():
    """
    GET /api/monthly
    คืนค่า: สถิติอุบัติเหตุแต่ละเดือน (ม.ค.–ธ.ค.)
    """
    rows = query_db("""
        SELECT
            เดือน,
            COUNT(*)                AS จำนวนครั้ง,
            SUM(จำนวนผู้เสียชีวิต)  AS ผู้เสียชีวิต
        FROM road_accidents
        GROUP BY เดือน
        ORDER BY เดือน
    """)
    return jsonify(rows)


# ======== Endpoint 4: สัดส่วนยานพาหนะ ========
@app.route('/api/vehicle-type')
def api_vehicle_type():
    """
    GET /api/vehicle-type
    คืนค่า: จำนวนอุบัติเหตุแยกตามประเภทยานพาหนะ
    """
    rows = query_db("""
        SELECT
            ยานพาหนะหลัก          AS ยานพาหนะ,
            COUNT(*)               AS จำนวน
        FROM road_accidents
        GROUP BY ยานพาหนะหลัก
        ORDER BY จำนวน DESC
    """)
    return jsonify(rows)


# ======== Endpoint 5: รายการอุบัติเหตุล่าสุด ========
@app.route('/api/recent')
def api_recent():
    """
    GET /api/recent
    คืนค่า: รายการอุบัติเหตุล่าสุด 20 รายการ
    """
    rows = query_db("""
        SELECT
            accident_id,
            วันที่เกิดเหตุ,
            จังหวัด,
            ยานพาหนะหลัก,
            ความรุนแรง,
            จำนวนผู้เสียชีวิต,
            จำนวนผู้บาดเจ็บรวม
        FROM road_accidents
        ORDER BY วันที่เกิดเหตุ DESC
        LIMIT 20
    """)
    return jsonify(rows)


# ======== Endpoint 6: ค้นหาตามจังหวัด (รับ parameter) ========
@app.route('/api/search')
def api_search():
    """
    GET /api/search?province=เชียงใหม่
    คืนค่า: อุบัติเหตุในจังหวัดที่ค้นหา (ปลอดภัยจาก SQL Injection)
    """
    from flask import request
    province = request.args.get('province', '')   # ← รับค่าจาก URL parameter

    if not province:
        return jsonify([])

    # ✅ ใช้ Parameterized Query — ปลอดภัย!
    rows = query_db("""
        SELECT accident_id, วันที่เกิดเหตุ, จังหวัด,
               ยานพาหนะหลัก, ความรุนแรง, จำนวนผู้เสียชีวิต
        FROM road_accidents
        WHERE จังหวัด = ?
        ORDER BY วันที่เกิดเหตุ DESC
        LIMIT 50
    """, (province,))   # ← ส่ง parameter แยก ไม่ต่อ String!

    return jsonify(rows)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## 🧪 ทดสอบ API ด้วยเบราว์เซอร์

เมื่อรัน `python app.py` แล้ว ลองเปิด URL เหล่านี้ในเบราว์เซอร์:

| URL | ผลที่ได้ |
|-----|---------|
| `http://localhost:5000/api/summary` | ตัวเลขสรุปรวม |
| `http://localhost:5000/api/by-province` | Top 10 จังหวัด |
| `http://localhost:5000/api/monthly` | รายเดือน |
| `http://localhost:5000/api/vehicle-type` | ยานพาหนะ |
| `http://localhost:5000/api/recent` | รายการล่าสุด |
| `http://localhost:5000/api/search?province=เชียงใหม่` | ค้นหาจังหวัด |

**ตัวอย่าง JSON Response จาก `/api/summary`:**
```json
{
  "total_accidents": 20000,
  "total_deaths": 471,
  "total_injured": 20573,
  "avg_injured_per_accident": 1.03
}
```

---

## 🔎 CORS — ทำไม JavaScript ถึงดึง API ได้

**CORS** (คอร์ส) ย่อมาจาก **Cross-Origin Resource Sharing** (ครอส-ออริจิน รีซอร์ส แชริ่ง) = การอนุญาตให้ Browser จาก Origin หนึ่งเรียก API ของอีก Origin ได้

ในโปรเจกต์นี้ Frontend และ Backend อยู่ที่ `localhost:5000` เดียวกัน จึงไม่มีปัญหา CORS แต่ถ้าแยก Server กัน ต้องเพิ่ม:

```python
# pip install flask-cors
from flask_cors import CORS
CORS(app)
```

---

# บทที่ 6.3 — สร้าง Frontend ด้วย HTML + Chart.js
**(6 ชั่วโมง)**

---

## 🌐 โครงสร้างไฟล์ HTML Dashboard

**Frontend** (ฟรอนต์เอนด์) = ส่วนที่ผู้ใช้มองเห็นและโต้ตอบกับเว็บ ประกอบด้วย:

- **HTML** (เอชทีเอ็มแอล) = โครงสร้าง (กระดูกของเว็บ)
- **CSS** (ซีเอสเอส) = สไตล์และสีสัน (ผิวหนังของเว็บ)
- **JavaScript** (จาวาสคริปต์) = พฤติกรรมและการโต้ตอบ (กล้ามเนื้อของเว็บ)

---

## 📄 ไฟล์ templates/index.html — ฉบับสมบูรณ์

```html
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard อุบัติเหตุทางถนน ปี 2568</title>
    <link rel="stylesheet" href="/static/style.css">
    <!-- Chart.js จากไฟล์ local (ออฟไลน์) -->
    <script src="/static/chart.min.js"></script>
</head>
<body>

    <!-- ===== HEADER ===== -->
    <header class="dashboard-header">
        <h1>🚗 Dashboard อุบัติเหตุทางถนน</h1>
        <p>ประเทศไทย ปี พ.ศ. 2568 | ข้อมูล: กรมทางหลวง</p>
    </header>

    <!-- ===== KPI CARDS (ตัวเลขสรุป) ===== -->
    <section class="kpi-section">
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-value" id="total-accidents">กำลังโหลด...</div>
            <div class="kpi-label">อุบัติเหตุรวม (ครั้ง)</div>
        </div>
        <div class="kpi-card danger">
            <div class="kpi-icon">💀</div>
            <div class="kpi-value" id="total-deaths">กำลังโหลด...</div>
            <div class="kpi-label">ผู้เสียชีวิต (ราย)</div>
        </div>
        <div class="kpi-card warning">
            <div class="kpi-icon">🤕</div>
            <div class="kpi-value" id="total-injured">กำลังโหลด...</div>
            <div class="kpi-label">ผู้บาดเจ็บ (ราย)</div>
        </div>
        <div class="kpi-card info">
            <div class="kpi-icon">📊</div>
            <div class="kpi-value" id="avg-injured">กำลังโหลด...</div>
            <div class="kpi-label">เฉลี่ยบาดเจ็บ/ครั้ง</div>
        </div>
    </section>

    <!-- ===== กราฟแถวบน ===== -->
    <section class="charts-row">

        <!-- Bar Chart: Top 10 จังหวัด -->
        <div class="chart-card">
            <h2>📊 10 จังหวัดที่มีอุบัติเหตุสูงสุด</h2>
            <canvas id="barChart"></canvas>
        </div>

        <!-- Pie Chart: ยานพาหนะ -->
        <div class="chart-card">
            <h2>🥧 สัดส่วนยานพาหนะที่เกิดอุบัติเหตุ</h2>
            <canvas id="pieChart"></canvas>
        </div>

    </section>

    <!-- ===== Line Chart: รายเดือน ===== -->
    <section class="chart-full">
        <div class="chart-card">
            <h2>📈 แนวโน้มอุบัติเหตุรายเดือน (ม.ค.–ธ.ค. 2568)</h2>
            <canvas id="lineChart"></canvas>
        </div>
    </section>

    <!-- ===== ตารางข้อมูล ===== -->
    <section class="table-section">
        <div class="table-header">
            <h2>📋 รายการอุบัติเหตุล่าสุด</h2>
            <div class="table-controls">
                <input type="text" id="searchInput"
                       placeholder="🔍 ค้นหาจังหวัด..." oninput="filterTable()">
                <button onclick="exportCSV()">📥 Export CSV</button>
            </div>
        </div>
        <div class="table-wrapper">
            <table id="accidentTable">
                <thead>
                    <tr>
                        <th>รหัส</th>
                        <th>วันที่</th>
                        <th>จังหวัด</th>
                        <th>ยานพาหนะ</th>
                        <th>ความรุนแรง</th>
                        <th>เสียชีวิต</th>
                        <th>บาดเจ็บ</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    <tr><td colspan="7">กำลังโหลดข้อมูล...</td></tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- ===== JavaScript ===== -->
    <script>

    // ======================================================
    // ส่วนที่ 1: โหลด KPI Cards
    // ======================================================
    async function loadSummary() {
        // fetch() คือการเรียก API — async/await รอผลก่อนทำต่อ
        const response = await fetch('/api/summary');
        const data = await response.json();

        // นำค่าใส่ใน HTML Element
        document.getElementById('total-accidents').textContent =
            data.total_accidents.toLocaleString();   // เพิ่ม , คั่นหลักพัน
        document.getElementById('total-deaths').textContent =
            data.total_deaths.toLocaleString();
        document.getElementById('total-injured').textContent =
            data.total_injured.toLocaleString();
        document.getElementById('avg-injured').textContent =
            data.avg_injured_per_accident;
    }


    // ======================================================
    // ส่วนที่ 2: Bar Chart — Top 10 จังหวัด
    // ======================================================
    async function loadBarChart() {
        const response = await fetch('/api/by-province');
        const data = await response.json();

        // แยก label และ value ออกจากกัน
        const labels = data.map(row => row['จังหวัด']);
        const values = data.map(row => row['จำนวนครั้ง']);
        const deaths = data.map(row => row['ผู้เสียชีวิต']);

        const ctx = document.getElementById('barChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',                    // ← ประเภทกราฟ
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'จำนวนอุบัติเหตุ (ครั้ง)',
                        data: values,
                        backgroundColor: 'rgba(54, 162, 235, 0.7)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'ผู้เสียชีวิต (ราย)',
                        data: deaths,
                        backgroundColor: 'rgba(255, 99, 132, 0.7)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }


    // ======================================================
    // ส่วนที่ 3: Pie Chart — ยานพาหนะ
    // ======================================================
    async function loadPieChart() {
        const response = await fetch('/api/vehicle-type');
        const data = await response.json();

        const labels = data.map(row => row['ยานพาหนะ']);
        const values = data.map(row => row['จำนวน']);

        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56',
            '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'
        ];

        const ctx = document.getElementById('pieChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: colors,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'right' }
                }
            }
        });
    }


    // ======================================================
    // ส่วนที่ 4: Line Chart — รายเดือน
    // ======================================================
    async function loadLineChart() {
        const response = await fetch('/api/monthly');
        const data = await response.json();

        const monthNames = [
            '', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
            'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'
        ];

        const labels = data.map(row => monthNames[row['เดือน']]);
        const accidents = data.map(row => row['จำนวนครั้ง']);
        const deaths = data.map(row => row['ผู้เสียชีวิต']);

        const ctx = document.getElementById('lineChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'จำนวนอุบัติเหตุ',
                        data: accidents,
                        borderColor: 'rgba(54, 162, 235, 1)',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        tension: 0.4,      // ← ความโค้งของเส้น
                        fill: true         // ← แรเงาใต้เส้น
                    },
                    {
                        label: 'ผู้เสียชีวิต',
                        data: deaths,
                        borderColor: 'rgba(255, 99, 132, 1)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.4,
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: 'top' }
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }


    // ======================================================
    // ส่วนที่ 5: ตารางข้อมูล
    // ======================================================
    let tableData = [];   // เก็บข้อมูลไว้สำหรับ Search และ Export

    async function loadTable() {
        const response = await fetch('/api/recent');
        tableData = await response.json();
        renderTable(tableData);
    }

    function renderTable(data) {
        const tbody = document.getElementById('tableBody');
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">ไม่พบข้อมูล</td></tr>';
            return;
        }

        // สร้าง HTML ของแถวข้อมูลทุกแถว
        tbody.innerHTML = data.map(row => `
            <tr>
                <td>${row['accident_id']}</td>
                <td>${row['วันที่เกิดเหตุ']}</td>
                <td>${row['จังหวัด']}</td>
                <td>${row['ยานพาหนะหลัก']}</td>
                <td class="severity-${row['ความรุนแรง']}">${row['ความรุนแรง']}</td>
                <td>${row['จำนวนผู้เสียชีวิต']}</td>
                <td>${row['จำนวนผู้บาดเจ็บรวม']}</td>
            </tr>
        `).join('');
    }


    // ======================================================
    // ส่วนที่ 6: Filter ตาราง (Search)
    // ======================================================
    function filterTable() {
        const keyword = document.getElementById('searchInput').value.toLowerCase();
        const filtered = tableData.filter(row =>
            row['จังหวัด'].toLowerCase().includes(keyword) ||
            row['ยานพาหนะหลัก'].toLowerCase().includes(keyword) ||
            row['ความรุนแรง'].toLowerCase().includes(keyword)
        );
        renderTable(filtered);
    }


    // ======================================================
    // ส่วนที่ 7: Export CSV
    // ======================================================
    function exportCSV() {
        if (tableData.length === 0) return;

        // สร้าง header
        const headers = Object.keys(tableData[0]);
        const csvRows = [
            headers.join(','),   // ← แถวหัวตาราง
            ...tableData.map(row =>
                headers.map(h => `"${row[h]}"`).join(',')
            )
        ];

        const csvContent = '\uFEFF' + csvRows.join('\n');   // \uFEFF = BOM สำหรับภาษาไทยใน Excel
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = 'accidents_export.csv';
        a.click();

        URL.revokeObjectURL(url);
        console.log('✅ Export CSV สำเร็จ!');
    }


    // ======================================================
    // เริ่มโหลดข้อมูลทั้งหมดเมื่อหน้าเว็บพร้อม
    // ======================================================
    window.onload = function() {
        loadSummary();
        loadBarChart();
        loadPieChart();
        loadLineChart();
        loadTable();
    };

    </script>

</body>
</html>
```

---

## 🎨 ไฟล์ static/style.css — ตกแต่ง Dashboard

```css
/* ===== RESET & BASE ===== */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, sans-serif;
    background-color: #f0f2f5;
    color: #333;
}

/* ===== HEADER ===== */
.dashboard-header {
    background: linear-gradient(135deg, #1a73e8, #0d47a1);
    color: white;
    padding: 20px 30px;
    text-align: center;
}

.dashboard-header h1 {
    font-size: 2rem;
    margin-bottom: 5px;
}

.dashboard-header p {
    opacity: 0.85;
    font-size: 0.95rem;
}

/* ===== KPI CARDS ===== */
.kpi-section {
    display: flex;                /* Flexbox — จัดการ layout */
    gap: 20px;
    padding: 25px 30px;
    flex-wrap: wrap;              /* ขึ้นบรรทัดใหม่ถ้าหน้าแคบ */
}

.kpi-card {
    flex: 1;
    min-width: 180px;
    background: white;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    border-left: 5px solid #1a73e8;
}

.kpi-card.danger  { border-left-color: #e53935; }
.kpi-card.warning { border-left-color: #fb8c00; }
.kpi-card.info    { border-left-color: #00897b; }

.kpi-icon  { font-size: 2rem; margin-bottom: 8px; }
.kpi-value { font-size: 2rem; font-weight: bold; color: #1a73e8; }
.kpi-card.danger  .kpi-value { color: #e53935; }
.kpi-card.warning .kpi-value { color: #fb8c00; }
.kpi-card.info    .kpi-value { color: #00897b; }
.kpi-label { font-size: 0.85rem; color: #666; margin-top: 5px; }

/* ===== CHART CARDS ===== */
.charts-row {
    display: flex;
    gap: 20px;
    padding: 0 30px 20px;
    flex-wrap: wrap;
}

.chart-card {
    flex: 1;
    min-width: 300px;
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.chart-card h2 {
    font-size: 1rem;
    margin-bottom: 15px;
    color: #444;
    border-bottom: 2px solid #f0f2f5;
    padding-bottom: 10px;
}

.chart-full {
    padding: 0 30px 20px;
}

.chart-full .chart-card {
    width: 100%;
}

/* ===== TABLE ===== */
.table-section {
    padding: 0 30px 30px;
}

.table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
    flex-wrap: wrap;
    gap: 10px;
}

.table-header h2 {
    font-size: 1rem;
    color: #444;
}

.table-controls {
    display: flex;
    gap: 10px;
}

.table-controls input {
    padding: 8px 14px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 0.9rem;
    width: 200px;
}

.table-controls button {
    padding: 8px 16px;
    background: #1a73e8;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
}

.table-controls button:hover {
    background: #1557b0;
}

.table-wrapper {
    background: white;
    border-radius: 12px;
    overflow-x: auto;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
}

thead th {
    background: #1a73e8;
    color: white;
    padding: 12px 15px;
    text-align: left;
    font-weight: 500;
}

tbody td {
    padding: 10px 15px;
    border-bottom: 1px solid #f0f2f5;
}

tbody tr:hover {
    background: #f8f9ff;
}

/* ความรุนแรง: สีตามระดับ */
.severity-เสียชีวิต    { color: #e53935; font-weight: bold; }
.severity-บาดเจ็บสาหัส { color: #fb8c00; font-weight: bold; }
.severity-บาดเจ็บเล็กน้อย { color: #43a047; }

/* ===== RESPONSIVE (มือถือ) ===== */
@media (max-width: 768px) {
    .kpi-section,
    .charts-row {
        flex-direction: column;    /* เรียงแนวตั้งบนจอแคบ */
    }

    .dashboard-header h1 {
        font-size: 1.4rem;
    }

    .kpi-section,
    .charts-row,
    .chart-full,
    .table-section {
        padding-left: 15px;
        padding-right: 15px;
    }
}
```

---

## 🔍 ทำความเข้าใจ `fetch()` และ `async/await`

**fetch()** (เฟ็ตช์) = คำสั่ง JavaScript ที่ใช้เรียกข้อมูลจาก URL (เรียก API)

**async/await** (อะซิงก์/อะเวท) = วิธีเขียนโค้ดที่รอผลก่อนทำขั้นต่อไป

```javascript
// แบบที่ 1: ไม่ใช้ async/await (ยากอ่าน)
fetch('/api/summary')
    .then(response => response.json())
    .then(data => {
        console.log(data);
    });

// แบบที่ 2: ใช้ async/await (อ่านง่ายกว่า — เหมือน Python)
async function loadData() {
    const response = await fetch('/api/summary');   // ← รอผลก่อน
    const data = await response.json();             // ← แปลง JSON ก่อน
    console.log(data);                              // ← แล้วค่อยใช้
}
```

**เปรียบเทียบ:** `await` เหมือนการบอกว่า "รอให้อาหารสุกก่อนนะ แล้วค่อยกิน" — ไม่ใช่รีบกินก่อนที่อาหารจะสุก

---

# บทที่ 6.4 — เพิ่มฟีเจอร์ขั้นสูง
**(3 ชั่วโมง)**

---

## 🔽 Filter ข้อมูลด้วย Dropdown

**Dropdown** (ดรอปดาวน์) = เมนูเลื่อนลงให้เลือก

เพิ่มลงใน `index.html` ส่วน table-controls:

```html
<!-- เพิ่ม Dropdown ในส่วน table-controls -->
<select id="regionFilter" onchange="filterByRegion()">
    <option value="">-- ทุกภูมิภาค --</option>
    <option value="ภาคเหนือ">ภาคเหนือ</option>
    <option value="ภาคกลาง">ภาคกลาง</option>
    <option value="ภาคตะวันออกเฉียงเหนือ">ภาคอีสาน</option>
    <option value="ภาคใต้">ภาคใต้</option>
    <option value="ภาคตะวันออก">ภาคตะวันออก</option>
</select>
```

เพิ่มฟังก์ชัน JavaScript:

```javascript
// ===== Filter ตามภูมิภาค =====
function filterByRegion() {
    const region = document.getElementById('regionFilter').value;

    if (region === '') {
        renderTable(tableData);   // ← แสดงทั้งหมด
        return;
    }

    // กรองข้อมูลจาก tableData ที่โหลดไว้แล้ว
    const filtered = tableData.filter(row =>
        row['ภูมิภาค'] === region
    );

    renderTable(filtered);
    console.log(`กรองข้อมูล: ${region} พบ ${filtered.length} รายการ`);
}
```

เพิ่ม Endpoint ใน `app.py` (Backend ดึงข้อมูลตามภูมิภาค):

```python
@app.route('/api/by-region')
def api_by_region():
    from flask import request
    region = request.args.get('region', '')

    if region:
        rows = query_db("""
            SELECT accident_id, วันที่เกิดเหตุ, จังหวัด, ภูมิภาค,
                   ยานพาหนะหลัก, ความรุนแรง,
                   จำนวนผู้เสียชีวิต, จำนวนผู้บาดเจ็บรวม
            FROM road_accidents
            WHERE ภูมิภาค = ?
            ORDER BY วันที่เกิดเหตุ DESC
            LIMIT 50
        """, (region,))
    else:
        rows = query_db("""
            SELECT accident_id, วันที่เกิดเหตุ, จังหวัด, ภูมิภาค,
                   ยานพาหนะหลัก, ความรุนแรง,
                   จำนวนผู้เสียชีวิต, จำนวนผู้บาดเจ็บรวม
            FROM road_accidents
            ORDER BY วันที่เกิดเหตุ DESC
            LIMIT 50
        """)
    return jsonify(rows)
```

---

## 🔍 Search ข้อมูลแบบ Real-time

Search ที่ทำไปแล้วใน `filterTable()` คือ **Client-side Search** — กรองจากข้อมูลที่โหลดมาแล้ว (เร็ว แต่ใช้ได้กับข้อมูลที่โหลดมาเท่านั้น)

สำหรับข้อมูลปริมาณมากต้องทำ **Server-side Search** — ส่งคำค้นไปที่ Server แล้วให้ SQL ค้นหา:

```javascript
// Search แบบ Server-side (ส่งไป Backend ค้นหา)
let searchTimer;   // ใช้ debounce ป้องกันเรียก API ทุกตัวอักษร

async function serverSearch() {
    const keyword = document.getElementById('searchInput').value;

    // Debounce: รอให้หยุดพิมพ์ 300ms ก่อนค้นหา
    clearTimeout(searchTimer);
    searchTimer = setTimeout(async () => {
        const response = await fetch(`/api/search?province=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        renderTable(data);
    }, 300);
}
```

---

## 📥 Export CSV — อธิบายเพิ่มเติม

ฟังก์ชัน `exportCSV()` ที่เขียนไปแล้วใน index.html ทำงานอย่างไร:

```
1. รับข้อมูลจาก tableData (array ใน memory)
2. แปลงเป็นรูปแบบ CSV (text คั่นด้วย comma)
3. เพิ่ม BOM (\uFEFF) ให้ Excel เปิดภาษาไทยได้
4. สร้าง Blob (ก้อนข้อมูลไบนารี)
5. สร้าง URL ชั่วคราวสำหรับ Blob
6. สร้าง <a> tag จำลอง แล้วคลิก → ดาวน์โหลด!
7. ลบ URL ชั่วคราวออก
```

---

## 📱 Responsive Design — ใช้งานได้บนมือถือ

**Responsive Design** (เรสปอนซิฟ ดีไซน์) = การออกแบบเว็บให้แสดงผลได้ดีทั้งบนคอมพิวเตอร์และมือถือ

CSS ที่ทำให้ Responsive คือส่วน `@media`:

```css
/* @media = กฎที่ใช้เฉพาะเมื่อหน้าจอกว้างไม่เกิน 768px (มือถือ) */
@media (max-width: 768px) {

    /* เปลี่ยน Flexbox จากแนวนอน → แนวตั้ง */
    .kpi-section,
    .charts-row {
        flex-direction: column;
    }

    /* ลดขนาดตัวอักษร */
    .dashboard-header h1 {
        font-size: 1.4rem;
    }
}
```

**เปรียบเทียบ Flexbox:**
```
บนคอมพิวเตอร์ (flex-direction: row):
[KPI 1] [KPI 2] [KPI 3] [KPI 4]  ← เรียงแนวนอน

บนมือถือ (flex-direction: column):
[KPI 1]
[KPI 2]
[KPI 3]
[KPI 4]  ← เรียงแนวตั้ง
```

---

# บทที่ 6.5 — นำเสนอ Mini Project
**(3 ชั่วโมง)**

---

## 🎤 แนวทางการนำเสนอ (10 นาที/กลุ่ม)

**โครงสร้างการนำเสนอที่ดี:**

```
นาทีที่ 1-2: แนะนำโปรเจกต์
   - Dashboard นี้ชื่ออะไร? ข้อมูลเกี่ยวกับอะไร?
   - ใครคือผู้ใช้งาน? (Target User)
   - แก้ปัญหาอะไร? ทำไมถึงทำ?

นาทีที่ 3-4: ที่มาของข้อมูล (Data Source)
   - ข้อมูลมาจากไหน?
   - มีกี่แถว กี่คอลัมน์?
   - ผ่านการตรวจสอบคุณภาพอย่างไร? (หน่วยที่ 3)

นาทีที่ 5-7: Demo Dashboard
   - เปิดเบราว์เซอร์ แสดง Dashboard จริง
   - อธิบาย KPI Card แต่ละตัว
   - อธิบายกราฟแต่ละอัน — ข้อค้นพบคืออะไร?
   - สาธิต Filter / Search / Export

นาทีที่ 8-9: เทคนิคที่ใช้
   - SQL ที่น่าสนใจ (JOIN, GROUP BY, Aggregate)
   - ความปลอดภัย (SQL Injection, PDPA)
   - ความท้าทายที่พบและแก้ไขอย่างไร?

นาทีที่ 10: สรุปและข้อเสนอแนะ
   - ข้อค้นพบสำคัญจากข้อมูล
   - ถ้ามีเวลาเพิ่ม จะพัฒนาอะไรต่อ?
   - คำถาม?
```

---

## ✅ เกณฑ์การประเมิน Mini Project (100 คะแนน)

| หัวข้อ | คะแนนเต็ม | เกณฑ์การให้คะแนน |
|--------|-----------|-----------------|
| **ฐานข้อมูล** | 20 | มีอย่างน้อย 3 ตาราง, ความสัมพันธ์ถูกต้อง, Primary/Foreign Key |
| **SQL** | 20 | ใช้ JOIN, GROUP BY, Aggregate Function ได้ถูกต้อง |
| **คุณภาพข้อมูล** | 15 | มีการตรวจสอบ NULL, Duplicate, รายงานผล |
| **Dashboard** | 25 | มีกราฟ ≥ 3 ประเภท, ตาราง, KPI Card, หน้าตาใช้งานง่าย |
| **ความปลอดภัย** | 10 | ใช้ Parameterized Query, ไม่เปิดเผยข้อมูลส่วนบุคคล |
| **การนำเสนอ** | 10 | อธิบายชัดเจน, ตอบคำถามได้, ใช้เวลาเหมาะสม |
| **รวม** | **100** | |

---

## 📋 Checklist ก่อนนำเสนอ

ตรวจสอบให้ครบก่อนส่งงาน:

```
ฐานข้อมูล:
☐ มีตาราง road_accidents นำเข้าสำเร็จ
☐ มีตารางอื่นอีกอย่างน้อย 2 ตาราง
☐ มี Primary Key ทุกตาราง
☐ มี Foreign Key เชื่อมตาราง (ถ้ามีความสัมพันธ์)

SQL:
☐ มีการใช้ GROUP BY อย่างน้อย 1 Query
☐ มีการใช้ COUNT / SUM / AVG
☐ มีการใช้ JOIN (ถ้ามีหลายตาราง)
☐ API ทุกตัวใช้ Parameterized Query

คุณภาพข้อมูล:
☐ ตรวจสอบ NULL แล้ว
☐ ตรวจสอบ Duplicate แล้ว
☐ มีรายงานสรุปคุณภาพข้อมูล (อย่างน้อยเป็นข้อความ)

Dashboard:
☐ Bar Chart ทำงานได้
☐ Line Chart ทำงานได้
☐ Pie/Doughnut Chart ทำงานได้
☐ ตารางข้อมูล แสดงได้
☐ KPI Card แสดงตัวเลขได้
☐ Search/Filter ใช้งานได้
☐ Export CSV ใช้งานได้

ความปลอดภัย:
☐ ทุก API ใช้ ? แทนการต่อ String
☐ ไม่มีข้อมูลส่วนบุคคลแสดงในตาราง
☐ Error handling เบื้องต้น

ไฟล์:
☐ README.md อธิบายโปรเจกต์
☐ app.py รันได้ไม่ Error
☐ index.html โหลดได้ทุก Chart
☐ โครงสร้างโฟลเดอร์ถูกต้อง
```

---

## 🐛 ปัญหาที่พบบ่อยและวิธีแก้

| ปัญหา | สาเหตุที่เป็นไปได้ | วิธีแก้ |
|-------|------------------|--------|
| กราฟไม่แสดง | `chart.min.js` ไม่ถูก path | ตรวจสอบ `/static/chart.min.js` |
| ภาษาไทยแสดงเป็น `???` | Encoding ผิด | เพิ่ม `encoding='utf-8-sig'` ตอนอ่าน CSV |
| API ส่งค่า null | ชื่อคอลัมน์ผิด | เปิด DB Browser ตรวจชื่อคอลัมน์ให้ตรง |
| Flask ไม่รัน | `import flask` ไม่ได้ | ติดตั้ง Flask อีกครั้ง |
| ตารางว่างเปล่า | fetch() ไม่สำเร็จ | กด F12 → Console ดู Error |
| Export CSV เปิดใน Excel เป็นอักขระแปลก | ขาด BOM | ตรวจสอบ `'\uFEFF'` ใน exportCSV() |

---

## 📊 สรุปเนื้อหาสำคัญหน่วยที่ 6

```
หน่วยที่ 6 — Mini Project: Dashboard ข้อมูลด้วย HTML

🏗️ สถาปัตยกรรม 3 ชั้น:
   Data Layer    → SQLite Database (school_data.db)
   Backend Layer → Python Flask (app.py) → ส่ง JSON
   Frontend Layer → HTML + CSS + JavaScript + Chart.js

📊 เลือกกราฟให้เหมาะสม:
   Bar Chart    → เปรียบเทียบหมวดหมู่
   Line Chart   → แนวโน้มตามเวลา
   Pie/Doughnut → สัดส่วนร้อยละ
   Table        → รายละเอียดข้อมูล

🐍 Flask Backend:
   @app.route('/api/...')  → กำหนด Endpoint
   query_db(sql, params)   → Query SQLite ปลอดภัย
   return jsonify(data)    → ส่งข้อมูลเป็น JSON

🌐 JavaScript Frontend:
   fetch('/api/...')        → เรียก API
   await response.json()   → รับข้อมูล JSON
   new Chart(ctx, {...})   → วาดกราฟด้วย Chart.js
   renderTable(data)        → สร้างตาราง Dynamic

⚡ ฟีเจอร์ขั้นสูง:
   Dropdown Filter → กรองตามเงื่อนไข
   Search          → ค้นหาแบบ Real-time
   Export CSV      → ดาวน์โหลดข้อมูล
   Responsive CSS  → รองรับมือถือ (@media)

🔐 ความปลอดภัย:
   ทุก SQL ใช้ ? (Parameterized Query)
   ไม่เปิดเผยข้อมูลส่วนบุคคล (PDPA)
   Error handling ป้องกัน Crash
```

---


---

## 🎓 สรุปทักษะที่ได้รับตลอดหลักสูตร 6 หน่วย

```
หน่วยที่ 1 → รู้จัก Big Data, ออกแบบ ERD, สร้างฐานข้อมูล SQLite
หน่วยที่ 2 → เขียน SQL ได้คล่อง SELECT / JOIN / GROUP BY / Aggregate
หน่วยที่ 3 → ตรวจสอบและทำความสะอาดข้อมูลด้วย Python + Pandas
หน่วยที่ 4 → รักษาความปลอดภัยข้อมูล CIA, PDPA, Hash, SQL Injection
หน่วยที่ 5 → จัดการ JSON และ NoSQL MongoDB ได้
หน่วยที่ 6 → สร้าง Dashboard ครบวงจร Flask + HTML + Chart.js

🏆 เป้าหมายสูงสุด: ออกแบบและสร้าง Data Dashboard จากข้อมูลจริงได้
    พร้อมต่อยอดสู่อาชีพ Data Analyst หรือ BI Developer
```

---

*หน่วยที่ 6 จบสมบูรณ์ — จบหลักสูตร การจัดการข้อมูลขนาดใหญ่เบื้องต้น Introduction to Big Data พ.ศ. 2026 🎉*
