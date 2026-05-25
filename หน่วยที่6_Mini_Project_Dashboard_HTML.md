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
5. เพิ่มฟีเจอร์ Filter หลายมิติ, Search, Pagination และ Export CSV ลงใน Dashboard ได้
6. ออกแบบ UI/UX Dashboard แบบ Modern Admin (Sidebar, KPI Cards, กราฟหลายมิติ) ได้
7. นำเสนอ Mini Project อธิบายที่มาของข้อมูล, SQL, คุณภาพ, และความปลอดภัยได้

> **ข้อมูลที่ใช้ตลอดหน่วยนี้:**
> ฐานข้อมูล `school_data.db` (SQLite) และ
> ข้อมูลอุบัติเหตุ `thailand_road_accidents_2568.csv` ที่เตรียมไว้ตลอดหลักสูตร
>
> **โฟลเดอร์ Lab พร้อมรัน:** `Lab/Lab-6/Lab6-mini_project/` (รัน `python setup_lab.py` ก่อน)

### ชื่อคอลัมน์จริงในตาราง `road_accidents` (สำคัญ)

เมื่อนำเข้าจาก CSV ชื่อคอลัมน์จะตรงกับไฟล์ต้นทาง — **ไม่ใช่** ชื่อย่อในเอกสารเก่า:

| ในเอกสาร/ตัวอย่างเก่า | ชื่อจริงใน SQLite (ใช้ใน SQL) |
|----------------------|------------------------------|
| `ยานพาหนะหลัก` | `ประเภทยานพาหนะหลัก` |
| `จำนวนผู้บาดเจ็บรวม` | `จำนวนผู้บาดเจ็บ` |

ใน Lab ใช้ `AS` ให้ JSON ยังใช้ชื่อสั้นใน Frontend ได้ เช่น  
`ประเภทยานพาหนะหลัก AS ยานพาหนะหลัก`

---

## โครงสร้างโปรเจกต์ (ภาพรวม)

**ใน Lab ใช้โฟลเดอร์:** `Lab/Lab-6/Lab6-mini_project/`

```
📁 Lab6-mini_project/
├── 📄 app.py                 ← Flask Backend + API ทั้งหมด
├── 📄 school_data.db         ← SQLite (สร้างจาก setup_lab.py)
├── 📁 static/
│   ├── 📄 style.css          ← Modern UI (สไตล์ Admin Dashboard)
│   ├── 📄 dashboard.js       ← โหลดข้อมูล, กราฟ, ตาราง, filter
│   └── 📄 chart.min.js       ← Chart.js (ออฟไลน์)
└── 📁 templates/
    └── 📄 index.html         ← โครงหน้า Sidebar + KPI + กราฟ + ตาราง
```

**อ้างอิง UI:** [Modernize Dashboard](https://modernize-react-main.netlify.app/dashboards/modern) — Sidebar, การ์ด KPI, กราฟ Grid, ตารางข้อมูลละเอียด

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
1. ผู้ใช้เปิดเบราว์เซอร์ → ไปที่ URL ที่ Flask แสดง (เช่น http://127.0.0.1:5000 หรือ :5050)
2. Flask ส่งไฟล์ index.html ให้เบราว์เซอร์
3. `dashboard.js` โหลด `/api/meta` แล้วเรียก `refreshAll()`
4. Flask รับคำขอพร้อมตัวกรอง → Query SQLite (Parameterized)
5. Flask ส่ง JSON กลับ (summary, กราฟ 7 ชุด, ตาราง accidents)
6. Chart.js วาดกราฟ + ตาราง 12 คอลัมน์ + KPI 6 ตัว
7. ผู้ใช้เปลี่ยนตัวกรอง → ทุกส่วนอัปเดตพร้อมกัน ✅
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
┌──────────┬───────────────────────────────────────────────────────────┐
│ SIDEBAR  │ TOPBAR: ชื่อ Dashboard | ค้นหา | รีเฟรช                    │
│ ภาพรวม   ├───────────────────────────────────────────────────────────┤
│ ตัวกรอง  │ KPI x6: อุบัติเหตุ | เสียชีวิต | บาดเจ็บ | เฉลี่ย | อัตราเสียชีวิต | จังหวัด │
│ กราฟ     ├───────────────────────────────────────────────────────────┤
│ ตาราง    │ แผงตัวกรอง: จังหวัด ภูมิภาค ความรุนแรง ยานพาหนะ ถนน เวลา เดือน │
│          ├────────────────────────────┬──────────────────────────────┤
│          │ กราฟจังหวัด (แนวนอน)       │ กราฟภูมิภาค (Doughnut)       │
│          ├──────────────┬─────────────┴──────────────────────────────┤
│          │ รายเดือน     │ ความรุนแรง (Polar)                        │
│          ├──────┬───────┴──────────────────────────────────────────────┤
│          │ ยานพาหนะ │ ประเภทถนน │ ช่วงเวลา กลางวัน/กลางคืน              │
│          ├───────────────────────────────────────────────────────────┤
│          │ ตาราง 12 คอลัมน์ | เลือก 25–500 แถว/หน้า | หน้า ถัดไป      │
└──────────┴───────────────────────────────────────────────────────────┘
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
cd Lab/Lab-6/Lab6-mini_project
pip install flask
python app.py
```

**ผลลัพธ์ใน Terminal:**
```
Dashboard: http://127.0.0.1:5000
 * Running on http://127.0.0.1:5000
```

> **Windows:** หลายเครื่องใช้พอร์ต **5000** ไม่ได้ (บริการ `iphlpsvc`) — สคริปต์ Lab จะสลับไป **5050** อัตโนมัติ ดู URL ที่ Terminal แสดง

เปิดเบราว์เซอร์ไปที่ URL ที่แสดง (เช่น `http://127.0.0.1:5050`)

---

## 🔌 สร้าง API Endpoint ที่ดึงข้อมูลจาก SQLite

**Endpoint** (เอนด์พอยท์) = URL แต่ละจุดที่ให้บริการข้อมูลต่างๆ

```python
# app.py — ฉบับสมบูรณ์สำหรับ Dashboard อุบัติเหตุ

from flask import Flask, jsonify, render_template, request
import sqlite3

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
            SUM(จำนวนผู้บาดเจ็บ)              AS total_injured,
            ROUND(AVG(จำนวนผู้บาดเจ็บ), 2)    AS avg_injured_per_accident
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
            SUM(จำนวนผู้บาดเจ็บ) AS ผู้บาดเจ็บ
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
            ประเภทยานพาหนะหลัก    AS ยานพาหนะ,
            COUNT(*)               AS จำนวน
        FROM road_accidents
        GROUP BY ประเภทยานพาหนะหลัก
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
            ภูมิภาค,
            ประเภทยานพาหนะหลัก AS ยานพาหนะหลัก,
            ความรุนแรง,
            จำนวนผู้เสียชีวิต,
            จำนวนผู้บาดเจ็บ AS จำนวนผู้บาดเจ็บรวม
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
    province = request.args.get('province', '')   # ← รับค่าจาก URL parameter

    if not province:
        return jsonify([])

    # ✅ ใช้ Parameterized Query — ปลอดภัย!
    rows = query_db("""
        SELECT accident_id, วันที่เกิดเหตุ, จังหวัด,
               ประเภทยานพาหนะหลัก AS ยานพาหนะหลัก, ความรุนแรง,
               จำนวนผู้เสียชีวิต
        FROM road_accidents
        WHERE จังหวัด = ?
        ORDER BY วันที่เกิดเหตุ DESC
        LIMIT 50
    """, (province,))   # ← ส่ง parameter แยก ไม่ต่อ String!

    return jsonify(rows)


if __name__ == '__main__':
    # Lab ตรวจพอร์ตก่อนรัน — ถ้า 5000 ไม่ว่าง (มักเป็น Windows) ใช้ 5050
    app.run(debug=True, port=5000, use_reloader=False)
```

> **โค้ดฉบับเต็ม** (12+ endpoints, `filter_clauses()`, `/api/meta`, `/api/accidents`, ตรวจพอร์ตอัตโนมัติ):  
> `Lab/Lab-6/Lab6-mini_project/app.py`  
> Frontend: `templates/index.html`, `static/dashboard.js`, `static/style.css`

---

## 🧪 ทดสอบ API ด้วยเบราว์เซอร์

เมื่อรัน `python app.py` แล้ว ดูพอร์ตใน Terminal (มักเป็น **5000** หรือ **5050** บน Windows) แล้วเปิด URL:

| URL | ผลที่ได้ |
|-----|---------|
| `http://127.0.0.1:5050/` | หน้า Modern Dashboard |
| `http://127.0.0.1:5050/api/meta` | ค่า dropdown |
| `http://127.0.0.1:5050/api/summary` | KPI 6 ตัว |
| `http://127.0.0.1:5050/api/by-province?province_limit=15` | จังหวัด Top N |
| `http://127.0.0.1:5050/api/by-region` | ภูมิภาค |
| `http://127.0.0.1:5050/api/accidents?limit=50&offset=0` | ตาราง + หน้า |
| `http://127.0.0.1:5050/api/summary?region=ภาคเหนือ` | ตัวอย่างกรอง |

ทดสอบไม่เปิดเบราว์เซอร์: `python Lab/Lab-6/Lab6-2_flask/test_api.py`

**ตัวอย่าง JSON Response จาก `/api/summary`:**
```json
{
  "total_accidents": 20000,
  "total_deaths": 471,
  "total_injured": 20573,
  "avg_injured_per_accident": 1.03,
  "province_count": 77,
  "fatal_cases": 471,
  "fatal_rate_pct": 2.36
}
```

---

## 📡 รายการ API ทั้งหมด (Lab 6)

ทุก endpoint รองรับ **ตัวกรองร่วม** ผ่าน query string (Parameterized Query):

| พารามิเตอร์ | คอลัมน์ใน DB | ตัวอย่าง |
|-------------|--------------|---------|
| `province` | จังหวัด | `?province=เชียงใหม่` |
| `region` | ภูมิภาค | `?region=ภาคเหนือ` |
| `severity` | ความรุนแรง | `?severity=เสียชีวิต` |
| `vehicle` | ประเภทยานพาหนะหลัก | `?vehicle=รถจักรยานยนต์` |
| `road_type` | ประเภทถนน | `?road_type=ทางหลวง` |
| `time_slot` | ช่วงเวลากลางวัน_กลางคืน | `?time_slot=กลางวัน` |
| `month` | เดือน (1–12) | `?month=7` |

| Endpoint | คำอธิบาย | พารามิเตอร์เพิ่ม |
|----------|----------|------------------|
| `GET /api/meta` | ค่า dropdown ทั้งหมด | — |
| `GET /api/summary` | KPI 6 ตัว | ตัวกรองร่วม |
| `GET /api/by-province` | จังหวัด Top N | `province_limit=15` |
| `GET /api/by-region` | สรุปภูมิภาค | ตัวกรองร่วม |
| `GET /api/monthly` | แนวโน้มรายเดือน | ตัวกรองร่วม |
| `GET /api/vehicle-type` | สัดส่วนยานพาหนะ | `limit` |
| `GET /api/severity` | ความรุนแรง | ตัวกรองร่วม |
| `GET /api/by-road-type` | ประเภทถนน Top 10 | ตัวกรองร่วม |
| `GET /api/by-time-slot` | กลางวัน/กลางคืน | ตัวกรองร่วม |
| `GET /api/accidents` | ตารางรายละเอียด | `limit`, `offset`, `q` (ค้นหา) |
| `GET /api/search` | ค้นหาจังหวัด (ตรง) | `province` |

**ตัวอย่างกรองหลายเงื่อนไข:**
```
/api/summary?region=ภาคเหนือ&severity=เสียชีวิต
/api/accidents?province=กรุงเทพมหานคร&limit=100&offset=0&q=ACC2568
```

**โค้ดตัวกรองใน Backend (แนวคิด):**
```python
def filter_clauses():
  mapping = {
    "province": "จังหวัด",
    "region": "ภูมิภาค",
    "severity": "ความรุนแรง",
    "vehicle": "ประเภทยานพาหนะหลัก",
    "road_type": "ประเภทถนน",
    "time_slot": "ช่วงเวลากลางวัน_กลางคืน",
  }
  parts, params = [], []
  for key, col in mapping.items():
    val = request.args.get(key, "").strip()
    if val:
      parts.append(f"{col} = ?")
      params.append(val)
  return parts, params
```

---

## 🔎 CORS — ทำไม JavaScript ถึงดึง API ได้

**CORS** (คอร์ส) ย่อมาจาก **Cross-Origin Resource Sharing** (ครอส-ออริจิน รีซอร์ส แชริ่ง) = การอนุญาตให้ Browser จาก Origin หนึ่งเรียก API ของอีก Origin ได้

ในโปรเจกต์นี้ Frontend และ Backend อยู่ที่ `localhost` พอร์ตเดียวกัน (5000 หรือ 5050) จึงไม่มีปัญหา CORS แต่ถ้าแยก Server กัน ต้องเพิ่ม:

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

## 🎨 Modern Dashboard UI (Lab 6)

**ไฟล์จริงใน Lab** (อ่านและแก้ไขจากที่นี่ — ไม่คัดลอกโค้ดยาวในเอกสาร):

| ไฟล์ | หน้าที่ |
|------|---------|
| `templates/index.html` | โครง Sidebar, KPI, แผงตัวกรอง, กราฟ 7 ชุด, ตาราง |
| `static/style.css` | สไตล์ Modern (สีหลัก `#5D87FF`, การ์ด, Grid) |
| `static/dashboard.js` | `fetch()` เรียก API, วาด Chart.js, pagination |
| `app.py` | Backend + filter ร่วมทุก endpoint |

### โครงสร้างหน้าเว็บ (index.html)

```html
<div class="app-shell">
  <aside class="sidebar">...</aside>
  <div class="main-wrapper">
    <header class="topbar">ค้นหา + ปุ่มรีเฟรช</header>
    <main class="content">
      <section id="overview">   <!-- KPI 6 การ์ด --></section>
      <section id="filters">    <!-- dropdown 7 มิติ --></section>
      <section id="charts">     <!-- กราฟ grid 7 ชุด --></section>
      <section id="datatable">  <!-- ตาราง 12 คอลัมน์ --></section>
    </main>
  </div>
</div>
<script src="/static/dashboard.js"></script>
```

### กราฟที่แสดง (dashboard.js)

| Canvas ID | ประเภท | ข้อมูลจาก API |
|-----------|--------|----------------|
| `chartProvince` | Bar แนวนอน | `/api/by-province` |
| `chartRegion` | Doughnut | `/api/by-region` |
| `chartMonthly` | Line | `/api/monthly` |
| `chartSeverity` | Polar Area | `/api/severity` |
| `chartVehicle` | Pie | `/api/vehicle-type` |
| `chartRoad` | Bar | `/api/by-road-type` |
| `chartTime` | Bar | `/api/by-time-slot` |

### CSS สำคัญ (style.css)

```css
:root {
  --primary: #5d87ff;      /* สีหลักแบบ Modernize */
  --bg: #f2f6fa;
  --surface: #ffffff;
}
.chart-canvas-wrap {
  height: 280px;           /* จำกัดความสูง — ไม่ให้กราฟยืดเต็มหน้า */
}
.charts-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
}
```

### JavaScript — โหลดและกรองข้อมูล

```javascript
// สร้าง query จากตัวกรองทุกตัว
function filterParams() {
  const p = new URLSearchParams();
  if (qs('f-province').value) p.set('province', qs('f-province').value);
  if (qs('f-region').value) p.set('region', qs('f-region').value);
  // ... severity, vehicle, road_type, time_slot, month
  return p;
}

async function refreshAll() {
  await loadKpis();      // GET /api/summary?...
  await loadCharts();    // เรียก API กราฟทุกตัวพร้อมกัน
  await loadTable();     // GET /api/accidents?limit=&offset=
}
```

เมื่อกด **ใช้ตัวกรอง** → ทุก KPI, กราฟ, ตารางอัปเดตตามเงื่อนไขเดียวกัน (Server-side filter)

### ตารางรายละเอียด (12 คอลัมน์)

| คอลัมน์ | ฟิลด์ JSON |
|---------|-----------|
| รหัส | `accident_id` |
| วันที่ / เวลา | `วันที่เกิดเหตุ`, `เวลาเกิดเหตุ` |
| สถานที่ | `จังหวัด`, `อำเภอ`, `ภูมิภาค` |
| ถนน / ยานพาหนะ | `ประเภทถนน`, `ยานพาหนะหลัก` |
| ผลกระทบ | `ความรุนแรง`, `ช่วงเวลา`, `จำนวนผู้เสียชีวิต`, `จำนวนผู้บาดเจ็บรวม` |

เลือกแสดง **25 / 50 / 100 / 200 / 500** แถวต่อหน้า — สูงสุด 500 แถว (`/api/accidents?limit=500&offset=0`)

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

# บทที่ 6.4 — ฟีเจอร์ขั้นสูง (Lab 6)
**(3 ชั่วโมง)**

---

## 🔽 Server-side Filter — กรองที่ Backend

**แนวคิด:** ส่งเงื่อนไขผ่าน URL → Flask สร้าง `WHERE` ด้วย `?` → ทุก KPI / กราฟ / ตารางได้ข้อมูลชุดเดียวกัน

**ใน Lab (`dashboard.js`):**
- โหลดค่า dropdown จาก `GET /api/meta`
- กด **ใช้ตัวกรอง** → เรียก `refreshAll()` ส่ง query เดียวกันทุก API
- แสดง **ชิป** เงื่อนไขที่เลือกอยู่ใต้แผงตัวกรอง

---

## 🔍 Search + Pagination

| ฟีเจอร์ | การทำงาน |
|---------|----------|
| ค้นหา | `q` ใน `/api/accidents` |
| Pagination | `limit` + `offset` (25–500 แถว/หน้า) |
| Debounce | รอหยุดพิมพ์ ~400ms ก่อนเรียก API |

---

## 📥 Export CSV + 📱 Modern UI

- Export หน้าปัจจุบัน + BOM ภาษาไทย
- Sidebar, Grid กราฟ, สี `#5D87FF` — อ้างอิง [Modernize Dashboard](https://modernize-react-main.netlify.app/dashboards/modern)
- ดู `Lab/Lab-6/TROUBLESHOOTING.md` (พอร์ต 5050 บน Windows)

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
☐ Modern UI (Sidebar + Topbar) แสดงถูกต้อง
☐ KPI 6 ตัว + กราฟ 7 ชุด ทำงานได้
☐ ตัวกรอง 7 มิติ อัปเดตทุกกราฟพร้อมกัน
☐ ตาราง 12 คอลัมน์ + Pagination (25–500 แถว)
☐ Search + Export CSV ใช้งานได้

ความปลอดภัย:
☐ ทุก API ใช้ ? แทนการต่อ String
☐ ไม่มีข้อมูลส่วนบุคคลแสดงในตาราง
☐ Error handling เบื้องต้น

ไฟล์:
☐ `python setup_lab.py` สำเร็จ
☐ `app.py` + `dashboard.js` + `style.css` ครบ
☐ เปิด Dashboard ได้ (ดูพอร์ตใน Terminal)
☐ `chart.min.js` อยู่ใน `static/`
```

---

## 🐛 ปัญหาที่พบบ่อยและวิธีแก้

| ปัญหา | สาเหตุที่เป็นไปได้ | วิธีแก้ |
|-------|------------------|--------|
| Flask ไม่รันที่พอร์ต 5000 | Windows ใช้พอร์ต 5000 (`iphlpsvc`) | ดู URL ใน Terminal (มักเป็น **5050**) หรือ `$env:PORT=5050; python app.py` |
| `UnicodeEncodeError` ตอน setup | Terminal Windows ใช้ cp1252 | `$env:PYTHONIOENCODING='utf-8'` ก่อนรัน หรือใช้ Lab ที่แก้แล้ว |
| กราฟไม่แสดง | `chart.min.js` ไม่ถูก path | รัน `python setup_lab.py` หรือคัดลอกไป `static/chart.min.js` |
| กราฟสูงเต็มหน้า | ไม่จำกัดความสูง canvas | ใช้ `.chart-canvas-wrap` + `maintainAspectRatio: false` |
| ภาษาไทยแสดงเป็น `???` | Encoding ผิด | เพิ่ม `encoding='utf-8-sig'` ตอนอ่าน CSV |
| API ส่งค่า null / Error | ชื่อคอลัมน์ผิด | ใช้ `ประเภทยานพาหนะหลัก`, `จำนวนผู้บาดเจ็บ` (ดูตารางด้านบน) |
| Flask ไม่รัน | `import flask` ไม่ได้ | `pip install flask` |
| ตารางว่างเปล่า | fetch() ไม่สำเร็จ / พอร์ตผิด | กด F12 → Console; ตรวจ URL ให้ตรงพอร์ตที่รัน |
| Export CSV เปิดใน Excel เป็นอักขระแปลก | ขาด BOM | ตรวจสอบ `'\uFEFF'` ใน exportCSV() |
| PowerShell ใช้ `&&` ไม่ได้ | เวอร์ชันเก่า | ใช้ `;` คั่นคำสั่ง หรือรันทีละบรรทัด |

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

🌐 JavaScript Frontend (dashboard.js):
   filterParams() + fetch()  → กรอง Server-side
   refreshAll()              → อัปเดต KPI + กราฟ + ตาราง
   Chart.js 7 ชุด           → วิเคราะห์หลายมิติ
   Pagination limit/offset   → ตารางละเอียด

⚡ ฟีเจอร์ขั้นสูง:
   Filter 7 มิติ + /api/meta
   Search (q) + Pagination
   Export CSV + Modern UI (Modernize style)
   พอร์ต 5050 fallback บน Windows

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
หน่วยที่ 6 → สร้าง Modern Dashboard Flask + Chart.js (กรองลึก, UI สวย)

🏆 เป้าหมายสูงสุด: ออกแบบและสร้าง Data Dashboard จากข้อมูลจริงได้
    พร้อมต่อยอดสู่อาชีพ Data Analyst หรือ BI Developer
```

---

*หน่วยที่ 6 จบสมบูรณ์ — จบหลักสูตร การจัดการข้อมูลขนาดใหญ่เบื้องต้น Introduction to Big Data พ.ศ. 2026 🎉*
