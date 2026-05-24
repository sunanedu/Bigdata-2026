# Lab หน่วยที่ 4 — ความปลอดภัยและการจัดการความเสี่ยงของข้อมูล

แบบฝึกปฏิบัติประกอบ [`หน่วยที่4_ความปลอดภัยและการจัดการความเสี่ยงของข้อมูล.md`](../../หน่วยที่4_ความปลอดภัยและการจัดการความเสี่ยงของข้อมูล.md)

**เครื่องมือ:** MySQL (GRANT), SQLite, Python hashlib

---

## เริ่มต้น

```powershell
cd C:\Users\ADMIN\Documents\GitHub\Bigdata-2026\Lab\Lab-4
python setup_lab.py
```

| ไฟล์ | ใช้กับ |
|------|--------|
| `output/school_security.db` | GRANT จำลอง, Login, Audit Log |
| `output/road_accidents.db` | SQL Injection ค้นหาปลอดภัย |
| `output/backups/` | ไฟล์สำรองจาก backup script |

**รหัสผ่านทดสอบ:** ดูใน `setup_lab.py` หลังรัน (เช่น `admin_it` / `Adm1n#Sup3r!`)

---

## Lab 4.1 — CIA Triad และ PDPA

[`Lab4-1_cia_pdpa_worksheet.md`](Lab4-1_cia_pdpa_worksheet.md)

---

## Lab 4.2 — การควบคุมการเข้าถึง (Workshop 4.2)

### MySQL (มี GRANT จริง)

1. สร้างฐานข้อมูล `school_db` จาก `schema.sql` + `seed.sql`
2. รัน [`mysql_grants.sql`](Lab4-2_access_control/mysql_grants.sql)
3. ทดสอบ `SHOW GRANTS FOR 'student_somjai'@'localhost';`

### SQLite (ใน Lab นี้)

```powershell
python Lab4-2_access_control/access_control.py
```

- ใช้ `views.sql` สำหรับ Row-Level Security (`v_grades_somjai`, `v_grades_child_daeng`)
- `access_control.py` จำลองสิทธิ์ตาม role

---

## Lab 4.3 — Risk Matrix (Workshop 4.3)

1. กรอก [`risk_matrix_template.md`](Lab4-3_risk_analysis/risk_matrix_template.md)
2. รัน `python Lab4-3_risk_analysis/risk_calculator.py`
3. อ้างอิงเฉลยครู: [`sample_risks_teacher.md`](Lab4-3_risk_analysis/sample_risks_teacher.md)

---

## Lab 4.4 — เทคโนโลยีป้องกัน (Workshop 4.4)

```powershell
python Lab4-4_security_tech/workshop_4_4.py
```

หรือรันแยกส่วน:

| สคริปต์ | เนื้อหา |
|--------|---------|
| `password_hash.py` | SHA-256 + Salt |
| `sql_injection_demo.py` | Unsafe vs Safe + Parameterized Query |
| `audit_log.py` | บันทึกและดู Log |
| `backup_database.py` | สำรอง 3-2-1 |

---

## โครงสร้าง

```
Lab/Lab-4/
├── README.md, Howto.txt, setup_lab.py
├── Lab4-1_cia_pdpa_worksheet.md
├── Lab4-2_access_control/
├── Lab4-3_risk_analysis/
├── Lab4-4_security_tech/
└── output/
```

---

## หมายเหตุ

- **SQLite ไม่มี GRANT** — ใช้ `mysql_grants.sql` บน MySQL จริง + `access_control.py` บน SQLite
- ข้อมูลอุบัติเหตุมีข้อมูลส่วนบุคคล — ฝึก PDPA และ Anonymize ก่อนเผยแพร่ Dashboard
