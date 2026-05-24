# Lab หน่วยที่ 2 — SQL สำหรับจัดการข้อมูลขนาดใหญ่

แบบฝึกปฏิบัติประกอบ [`หน่วยที่2_SQL_สำหรับจัดการข้อมูลขนาดใหญ่.md`](../../หน่วยที่2_SQL_สำหรับจัดการข้อมูลขนาดใหญ่.md)

**เครื่องมือ:** SQLite, DB Browser for SQLite, Python 3 + pandas

---

## เริ่มต้น

```powershell
cd C:\Users\ADMIN\Documents\GitHub\Bigdata-2026\Lab\Lab-2
python setup_lab.py
```

| ไฟล์ใน `output/` | ใช้กับ Lab |
|-------------------|------------|
| `ddl_students.db` | 2.1 DDL & DML |
| `road_accidents.db` | 2.2, 2.4, 2.5 (20,000 แถว) |
| `school_join.db` | 2.3 JOIN |
| `bank_demo.db` | 2.4 TRANSACTION |

---

## Lab 2.1 — DDL & DML (Workshop 2.1)

โฟลเดอร์: [`Lab2-1_ddl_dml/`](Lab2-1_ddl_dml/)

1. เปิด `output/ddl_students.db` ใน DB Browser
2. รัน [`workshop.sql`](Lab2-1_ddl_dml/workshop.sql) ตามเอกสาร
3. ทำแบบฝึก [`exercises.sql`](Lab2-1_ddl_dml/exercises.sql)
4. ตรวจคำตอบ [`solutions.sql`](Lab2-1_ddl_dml/solutions.sql) (ครู)

---

## Lab 2.2 — SELECT ขั้นสูง (Workshop 2.2)

โฟลเดอร์: [`Lab2-2_select_analysis/`](Lab2-2_select_analysis/)

1. เปิด `output/road_accidents.db`
2. รัน [`workshop.sql`](Lab2-2_select_analysis/workshop.sql) — Top 5 สาเหตุ, กลางคืน, วันหยุด
3. ทำ [`exercises.sql`](Lab2-2_select_analysis/exercises.sql)
4. เฉลย: [`solutions.sql`](Lab2-2_select_analysis/solutions.sql)

---

## Lab 2.3 — JOIN (Workshop 2.3)

โฟลเดอร์: [`Lab2-3_join/`](Lab2-3_join/)

1. เปิด `output/school_join.db` (students + subjects + enrollments)
2. รัน [`workshop.sql`](Lab2-3_join/workshop.sql) — JOIN 3 ตาราง + CASE เกรด
3. ทำ [`exercises.sql`](Lab2-3_join/exercises.sql) — INNER, LEFT, GROUP BY, Subquery

---

## Lab 2.4 — VIEW, INDEX, TRANSACTION (บท 2.4)

โฟลเดอร์: [`Lab2-4_view_index_transaction/`](Lab2-4_view_index_transaction/)

- `road_accidents.db` มี VIEW `v_province_summary` และ INDEX แล้ว (จาก `setup_lab.py`)
- รัน [`views.sql`](Lab2-4_view_index_transaction/views.sql) เพิ่มเติมได้
- ทดลอง TRANSACTION กับ [`transaction_demo.sql`](Lab2-4_view_index_transaction/transaction_demo.sql) + `bank_demo.db`

---

## Lab 2.5 — Python Pipeline (Workshop 2.5)

```powershell
pip install pandas
python Lab2-5_python_pipeline/pipeline.py
```

ผลลัพธ์ใน `output/exports/`:

- `accidents_clean.csv`
- `province_summary.csv` / `.json`
- `summary_by_province.json` (ใช้หน่วยที่ 6 Dashboard ได้)

---

## โครงสร้าง

```
Lab/Lab-2/
├── README.md
├── Howto.txt
├── setup_lab.py
├── Lab2-1_ddl_dml/
├── Lab2-2_select_analysis/
├── Lab2-3_join/
├── Lab2-4_view_index_transaction/
├── Lab2-5_python_pipeline/
└── output/
```

---

## เงื่อนไขก่อนเริ่ม

- ควรทำ Lab 1 แล้ว (มี `road_accidents.db`) หรือมี `data/thailand_road_accidents_2568.csv`
- `setup_lab.py` จะคัดลอกจาก Lab-1 หรือ import CSV อัตโนมัติ
