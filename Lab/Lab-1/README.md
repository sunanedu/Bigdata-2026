# Lab หน่วยที่ 1 — พื้นฐาน Big Data และระบบฐานข้อมูล

แบบฝึกปฏิบัติประกอบเอกสาร [`หน่วยที่1_พื้นฐาน_BigData_และระบบฐานข้อมูล.md`](../../หน่วยที่1_พื้นฐาน_BigData_และระบบฐานข้อมูล.md)

**เครื่องมือ:** DB Browser for SQLite, Python 3 (ไม่บังคับ)

---

## โครงสร้างโฟลเดอร์

```
Lab-1/
├── README.md                 ← คู่มือนี้
├── setup_lab.py              ← สร้างฐานข้อมูลทั้งหมดใน output/
├── data/
│   ├── students.csv          ← 20 นักเรียน (หน่วยที่ 2)
│   └── products.csv          ← รายการสินค้าตัวอย่าง
├── Lab1-1_5V_worksheet.md    ← แบบฝึก 5V (ทฤษฎี)
├── Lab1-2_first_database/    ← Workshop 1.2
├── Lab1-3_shop_erd/          ← Workshop 1.3
├── Lab1-4_csv_import/        ← บทที่ 1.4
└── output/                   ← ฐานข้อมูลที่สร้างแล้ว (รัน setup ก่อน)
```

---

## เริ่มต้นอย่างรวดเร็ว

```powershell
cd C:\Users\ADMIN\Documents\GitHub\Bigdata-2026\Lab\Lab-1
python setup_lab.py
```

ไฟล์ที่ได้ใน `output/`:

| ไฟล์ | เนื้อหา |
|------|---------|
| `my_first_database.db` | ตาราง `students` (Lab 1.2) |
| `shop_database.db` | ร้านป้าแดง 4 ตาราง (Lab 1.3) |
| `school_system.db` | นักเรียน + วิชา + การลงทะเบียน |
| `road_accidents.db` | ข้อมูลอุบัติเหตุ (Lab 1.4) |

เปิดด้วย **DB Browser for SQLite** → Open Database → เลือกไฟล์ใน `output/`

---

## Lab 1.1 — หลักการ 5V

- ทำแบบฝึกใน [`Lab1-1_5V_worksheet.md`](Lab1-1_5V_worksheet.md)
- อ้างอิงบทที่ 1.1 ในเอกสารหลัก

---

## Lab 1.2 — สร้างฐานข้อมูลแรก (Workshop 1.2)

### วิธี A: DB Browser (ตามเอกสาร)

1. New Database → บันทึกเป็น `my_first_database.db`
2. Execute SQL จาก [`Lab1-2_first_database/schema.sql`](Lab1-2_first_database/schema.sql)
3. Execute SQL จาก [`seed.sql`](Lab1-2_first_database/seed.sql)
4. ลองคำสั่ง:

```sql
SELECT * FROM students;
SELECT name, score FROM students WHERE grade = 10 ORDER BY score DESC;
```

### วิธี B: ใช้สคริปต์

```powershell
python setup_lab.py
```

---

## Lab 1.3 — ERD ร้านป้าแดง (Workshop 1.3)

1. อ่านแผนภาพใน [`Lab1-3_shop_erd/erd_shop.txt`](Lab1-3_shop_erd/erd_shop.txt)
2. สร้างตารางด้วย [`schema.sql`](Lab1-3_shop_erd/schema.sql) + ข้อมูล [`seed.sql`](Lab1-3_shop_erd/seed.sql)
3. ทดสอบ Foreign Key:

```sql
SELECT c.cust_name, o.order_date, p.prod_name, oi.quantity, oi.unit_price
FROM orders o
JOIN customers c ON o.cust_id = c.cust_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
```

---

## Lab 1.4 — นำเข้า CSV (บทที่ 1.4)

### วิธี A: DB Browser

1. New Database → `road_accidents.db`
2. File → Import → Table from CSV
3. เลือก `thailand_road_accidents_2568_fix.csv` (วางไว้ที่ `data/` ใน repo)
4. ชื่อตาราง: `road_accidents`, Encoding UTF-8, แถวแรกเป็นชื่อคอลัมน์

### วิธี B: Python

```powershell
# ถ้ามี CSV ชุดเต็ม (~20,000 แถว)
python Lab1-4_csv_import/import_road_accidents.py --csv ..\..\data\thailand_road_accidents_2568_fix.csv

# ถ้ายังไม่มี CSV — ใช้ตัวอย่างจาก data/school_data.db
python Lab1-4_csv_import/import_road_accidents.py --from-school-db
```

ตรวจสอบด้วย [`Lab1-4_csv_import/verify.sql`](Lab1-4_csv_import/verify.sql)

| รายการ | ชุดเต็ม (CSV) | ตัวอย่างใน repo |
|--------|---------------|-----------------|
| จำนวนแถว | ~20,000 | ~5,000 |
| คอลัมน์ | 51 | 51 |

---

## ไฟล์ข้อมูลที่ครูเตรียม

| ไฟล์ | ที่อยู่ |
|------|--------|
| `students.csv` | `Lab/Lab-1/data/` |
| `products.csv` | `Lab/Lab-1/data/` |
| `school_data.db` | `data/` (ข้อมูลอุบัติเหตุตัวอย่าง) |
| `thailand_road_accidents_2568_fix.csv` | วางที่ `data/` (ชื่อ จังหวัด/อำเภอ/ตำบล แก้แล้ว, 52 คอลัมน์) |

---

## เชื่อมโยงหน่วยถัดไป

หลังทำ Lab 1 เสร็จ ใช้ `output/road_accidents.db` หรือ `data/school_data.db` ในหน่วยที่ 2 (SQL)
