# Lab หน่วยที่ 3 — คุณภาพข้อมูลและการตรวจสอบ

แบบฝึกปฏิบัติประกอบ [`หน่วยที่3_คุณภาพข้อมูลและการตรวจสอบ.md`](../../หน่วยที่3_คุณภาพข้อมูลและการตรวจสอบ.md)

**เครื่องมือ:** SQLite, DB Browser, Python 3 + Pandas

---

## เริ่มต้น

```powershell
cd C:\Users\ADMIN\Documents\GitHub\Bigdata-2026\Lab\Lab-3
python setup_lab.py
```

| ไฟล์ | ใช้กับ |
|------|--------|
| `output/road_accidents.db` | Lab 3.2 SQL (ข้อมูล 20,000 แถว) |
| `data/dirty_records.csv` | Lab 3.2–3.4 (ข้อมูลมีปัญหาเจตนา) |
| `output/dirty_records.db` | SQL บนตาราง dirty (import แล้ว) |

---

## Lab 3.1 — 6 มิติคุณภาพข้อมูล

[`Lab3-1_6dimensions_worksheet.md`](Lab3-1_6dimensions_worksheet.md)

---

## Lab 3.2 — ตรวจสอบด้วย SQL (Workshop 3.2)

โฟลเดอร์: [`Lab3-2_sql_checks/`](Lab3-2_sql_checks/)

1. เปิด `output/road_accidents.db`
2. รัน [`workshop_10_checks.sql`](Lab3-2_sql_checks/workshop_10_checks.sql) — 10 ข้อตามเอกสาร
3. รัน [`checks_overview.sql`](Lab3-2_sql_checks/checks_overview.sql) — 6 ขั้นตรวจสอบ
4. เปิด `output/dirty_records.db` ทำ [`exercises.sql`](Lab3-2_sql_checks/exercises.sql)

---

## Lab 3.3 — ทำความสะอาดด้วย Pandas (Workshop 3.3)

```powershell
pip install pandas

# ทำความสะอาด dirty_records → clean_records.csv
python Lab3-3_pandas_cleaning/clean_dirty_records.py

# Pipeline ชุดใหญ่ road_accidents → road_accidents_cleaned.csv
python Lab3-3_pandas_cleaning/clean_road_accidents.py
```

เกณฑ์ `clean_records.csv`:

1. ไม่มี NULL ใน `จังหวัด`, `ความรุนแรง`, `อายุ_ปี`
2. ไม่มี `accident_id` ซ้ำ
3. `อายุ_ปี` อยู่ 5–100
4. `เดือน` อยู่ 1–12
5. ข้อความไม่มีช่องว่างหัวท้าย

---

## Lab 3.4 — Data Quality Report (Workshop 3.4)

```powershell
python Lab3-4_dq_report/generate_dq_report.py
python Lab3-4_dq_report/generate_dq_report.py --file output/road_accidents_cleaned.csv

# ตารางสรุป ก่อน/หลัง (dirty vs clean)
python Lab3-4_dq_report/compare_before_after.py
```

เปิดรายงาน: `output/reports/dq_report.html`

---

## โครงสร้าง

```
Lab/Lab-3/
├── README.md, Howto.txt, setup_lab.py
├── data/dirty_records.csv
├── Lab3-1_6dimensions_worksheet.md
├── Lab3-2_sql_checks/
├── Lab3-3_pandas_cleaning/
├── Lab3-4_dq_report/
└── output/
```

---

## เงื่อนไขก่อนเริ่ม

- ควรมี `road_accidents.db` จาก Lab 1 หรือ Lab 2 (หรือ CSV ใน `data/`)
- `setup_lab.py` สร้าง `dirty_records` อัตโนมัติ
