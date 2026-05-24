# การจัดการข้อมูลขนาดใหญ่เบื้องต้น
## Introduction to Big Data (พ.ศ. 2026)

> **จำนวน:** 6 หน่วย | **เวลาเรียนทั้งหมด:** 75 ชั่วโมง  
> **อุปกรณ์:** Computer PC i5 | RAM 8 GB | SSD 256 GB | Windows 10 Pro  
> **หมายเหตุ:** อินเทอร์เน็ตช้า — ครูเตรียมไฟล์ทั้งหมดลงแฟลชไดร์ฟให้นักเรียน

---

## ทำไมต้องเรียน Big Data ในปี 2026?

ในยุคที่ข้อมูลเติบโตอย่างรวดเร็ว ทักษะการจัดการข้อมูลขนาดใหญ่กลายเป็นสิ่งจำเป็นในทุกสาขาอาชีพ ผู้ที่เข้าใจ Big Data จะสามารถ:

- **วิเคราะห์และตัดสินใจ** จากข้อมูลจริงแทนการคาดเดา
- **ออกแบบระบบฐานข้อมูล** ที่มีประสิทธิภาพและปลอดภัย
- **นำเสนอข้อมูล** ผ่าน Dashboard ที่เข้าใจง่าย
- **ต่อยอดสู่อาชีพ** Data Analyst, Data Engineer, BI Developer

---

## เรียนแล้วได้อะไร?

| ทักษะ | รายละเอียด |
|-------|-----------|
| ด้านเทคนิค | เขียน SQL ได้คล่อง, ใช้ Python/Pandas ได้, สร้าง Dashboard ด้วย HTML ได้ |
| ด้านการคิด | ตรวจสอบคุณภาพข้อมูล, วิเคราะห์ความเสี่ยง, ออกแบบโครงสร้างข้อมูล |
| Mini Project | สร้าง Dashboard ที่ดึงข้อมูลจากฐานข้อมูลจริงมาแสดงผลแบบ Real-time |

---

## เครื่องมือหลักที่ใช้ในหลักสูตรนี้ (Tools 2026)

| หมวด | เครื่องมือ | เหตุผลที่เลือก |
|------|-----------|---------------|
| ฐานข้อมูล | **SQLite** / **MySQL Community** | เบา, ใช้ได้ออฟไลน์, ไม่ต้องการเซิร์ฟเวอร์ |
| ภาษา Query | **SQL (Standard)** | มาตรฐานอุตสาหกรรม ใช้กับทุก RDBMS |
| วิเคราะห์ข้อมูล | **Python 3 + Pandas + Jupyter Notebook** | ฟรี, ชุมชนใหญ่, ใช้ได้ออฟไลน์ |
| Dashboard / นำเสนอ | **HTML + CSS + JavaScript (Chart.js)** | ทำงานได้โดยไม่ต้องใช้อินเทอร์เน็ต |
| เครื่องมือ NoSQL | **MongoDB Community** | ข้อมูลไม่มีโครงสร้าง (Unstructured) |
| IDE / Editor | **VS Code** | ฟรี, รองรับทุก tool ที่ใช้ |
| จัดการไฟล์ข้อมูล | **CSV, JSON, Excel (openpyxl)** | รูปแบบข้อมูลที่พบบ่อยในชีวิตจริง |

---

## ภาพรวมหลักสูตร 6 หน่วย

```
หน่วยที่ 1 → พื้นฐาน Big Data & ระบบฐานข้อมูล        (12 ชั่วโมง)
หน่วยที่ 2 → SQL สำหรับจัดการข้อมูล                  (15 ชั่วโมง)
หน่วยที่ 3 → คุณภาพและการตรวจสอบข้อมูล               (10 ชั่วโมง)
หน่วยที่ 4 → ความปลอดภัยและความเสี่ยงของข้อมูล        (10 ชั่วโมง)
หน่วยที่ 5 → ข้อมูลไม่มีโครงสร้าง (Unstructured Data) (10 ชั่วโมง)
หน่วยที่ 6 → Mini Project: สร้าง Dashboard ด้วย HTML  (18 ชั่วโมง)
                                              รวม 75 ชั่วโมง
```

---

## หน่วยที่ 1: พื้นฐาน Big Data และระบบฐานข้อมูล
**เวลา: 12 ชั่วโมง**

### จุดประสงค์
นักเรียนเข้าใจแนวคิด Big Data, ความแตกต่างของระบบฐานข้อมูล และสามารถออกแบบโครงสร้างฐานข้อมูลเบื้องต้นได้

### เนื้อหา

#### 1.1 Big Data คืออะไร? (2 ชั่วโมง)
- นิยาม Big Data และ 5V: Volume, Velocity, Variety, Veracity, Value
- ตัวอย่างข้อมูลขนาดใหญ่ในชีวิตจริง (โซเชียลมีเดีย, โรงพยาบาล, ห้างสรรพสินค้า)
- วงจรชีวิตของข้อมูล (Data Lifecycle): เก็บ → ประมวลผล → วิเคราะห์ → นำเสนอ
- แนวโน้ม Big Data ในปี 2026

#### 1.2 ระบบฐานข้อมูล (Database Systems) (4 ชั่วโมง)
- ความแตกต่างระหว่าง **Relational Database (SQL)** และ **Non-Relational (NoSQL)**
- ประเภทของฐานข้อมูล: MySQL, SQLite, MongoDB, Redis
- **Workshop:** ติดตั้ง SQLite + DB Browser for SQLite (ออฟไลน์)
- สร้างฐานข้อมูลใหม่ด้วยมือครั้งแรก

#### 1.3 การออกแบบโครงสร้างฐานข้อมูล (4 ชั่วโมง)
- Entity Relationship Diagram (ERD) เบื้องต้น
- Primary Key, Foreign Key, Relationship (1:1, 1:N, M:N)
- Normalization (1NF, 2NF, 3NF) ทำไมต้องแยกตาราง?
- **Workshop:** ออกแบบ ERD สำหรับระบบร้านค้า / โรงเรียน

#### 1.4 เตรียมข้อมูลสำหรับหน่วยต่อไป (2 ชั่วโมง)
- นำเข้าข้อมูล CSV ลง SQLite
- ทำความเข้าใจโครงสร้างตัวอย่างข้อมูลที่ใช้ตลอดหลักสูตร
- **ไฟล์ที่ครูเตรียม:** `school_data.db`, `students.csv`, `products.csv`

---

## หน่วยที่ 2: SQL สำหรับจัดการข้อมูลขนาดใหญ่
**เวลา: 15 ชั่วโมง**

### จุดประสงค์
นักเรียนสามารถเขียนคำสั่ง SQL เพื่อ สร้าง, ค้นหา, แก้ไข, วิเคราะห์ และสรุปข้อมูลได้

### เนื้อหา

#### 2.1 คำสั่ง SQL พื้นฐาน — DDL & DML (3 ชั่วโมง)
- **DDL:** `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`
- **DML:** `INSERT`, `UPDATE`, `DELETE`
- ประเภทข้อมูล: `INTEGER`, `TEXT`, `REAL`, `BLOB`, `DATE`
- **Workshop:** สร้างตารางนักเรียน + เพิ่มข้อมูล 20 แถว

#### 2.2 การค้นหาข้อมูล — SELECT ขั้นสูง (4 ชั่วโมง)
- `SELECT`, `WHERE`, `ORDER BY`, `LIMIT`
- `AND`, `OR`, `NOT`, `BETWEEN`, `LIKE`, `IN`
- `GROUP BY`, `HAVING`
- `DISTINCT`, `COUNT`, `SUM`, `AVG`, `MAX`, `MIN`
- **Workshop:** วิเคราะห์ข้อมูลยอดขายจากตัวอย่างร้านค้า

#### 2.3 การเชื่อมตาราง — JOIN (4 ชั่วโมง)
- `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`
- การ JOIN หลายตาราง
- Subquery (คำสั่งซ้อนใน WHERE และ FROM)
- **Workshop:** ดึงข้อมูลนักเรียน + ผลการเรียน + รายวิชา จาก 3 ตาราง

#### 2.4 View, Index และ Transaction (2 ชั่วโมง)
- สร้าง `VIEW` เพื่อใช้งานซ้ำ
- `INDEX` ช่วยให้ค้นหาเร็วขึ้นอย่างไร?
- `TRANSACTION`, `COMMIT`, `ROLLBACK`

#### 2.5 เชื่อมต่อฐานข้อมูลด้วย Python (2 ชั่วโมง)
- ใช้ `sqlite3` library ใน Python
- ดึงข้อมูลจาก SQLite → Pandas DataFrame
- Export ผลลัพธ์เป็น CSV/JSON เพื่อใช้ใน Dashboard

---

## หน่วยที่ 3: คุณภาพข้อมูลและการตรวจสอบ
**เวลา: 10 ชั่วโมง**

### จุดประสงค์
นักเรียนสามารถระบุปัญหาคุณภาพข้อมูล, ทำความสะอาดข้อมูล และสรุปผลการตรวจสอบได้อย่างเป็นระบบ

### เนื้อหา

#### 3.1 มิติของคุณภาพข้อมูล (2 ชั่วโมง)
- **6 มิติหลัก:** ความถูกต้อง (Accuracy), ความสมบูรณ์ (Completeness), ความสอดคล้อง (Consistency), ความทันสมัย (Timeliness), ความเป็นเอกลักษณ์ (Uniqueness), ความถูกต้องตามรูปแบบ (Validity)
- ปัญหาที่พบบ่อย: ข้อมูลซ้ำ, ค่าว่าง (NULL), รูปแบบไม่ตรง, ค่าผิดปกติ (Outlier)
- ผลกระทบของข้อมูลคุณภาพต่ำต่อการตัดสินใจ

#### 3.2 การตรวจสอบคุณภาพด้วย SQL (3 ชั่วโมง)
- หา NULL: `WHERE column IS NULL`
- หาข้อมูลซ้ำ: `GROUP BY ... HAVING COUNT(*) > 1`
- ตรวจสอบรูปแบบ: `LIKE`, `LENGTH()`
- ตรวจสอบช่วงค่า: `CHECK` constraint
- **Workshop:** ตรวจสอบไฟล์ข้อมูลจริงที่มีปัญหา 10 ประเภท

#### 3.3 การทำความสะอาดข้อมูลด้วย Python + Pandas (3 ชั่วโมง)
- `df.isnull()`, `df.dropna()`, `df.fillna()`
- `df.duplicated()`, `df.drop_duplicates()`
- แปลงประเภทข้อมูล: `astype()`, `pd.to_datetime()`
- Standardize ข้อมูลข้อความ: `.strip()`, `.lower()`, `.replace()`
- **Workshop:** ทำความสะอาดไฟล์ CSV ที่มีปัญหา → บันทึกเป็นไฟล์ใหม่

#### 3.4 รายงานสรุปคุณภาพข้อมูล (Data Quality Report) (2 ชั่วโมง)
- โครงสร้างรายงาน: สถิติเบื้องต้น, ปัญหาที่พบ, วิธีแก้ไข, ผลหลังทำความสะอาด
- สร้าง Data Quality Report อัตโนมัติด้วย Python (`df.describe()`, `df.info()`)
- **Workshop:** จัดทำรายงานคุณภาพข้อมูลเป็น HTML

---

## หน่วยที่ 4: ความปลอดภัยและการจัดการความเสี่ยงของข้อมูล
**เวลา: 10 ชั่วโมง**

### จุดประสงค์
นักเรียนเข้าใจหลักการรักษาความปลอดภัยข้อมูล สามารถระบุความเสี่ยง และนำเสนอมาตรการป้องกันได้

### เนื้อหา

#### 4.1 หลักการความปลอดภัยข้อมูล (2 ชั่วโมง)
- CIA Triad: **Confidentiality** (ความลับ), **Integrity** (ความถูกต้อง), **Availability** (ความพร้อมใช้)
- กฎหมาย PDPA (พ.ร.บ. คุ้มครองข้อมูลส่วนบุคคล พ.ศ. 2562) เบื้องต้น
- ประเภทข้อมูลที่ต้องการการปกป้องพิเศษ (ข้อมูลส่วนบุคคล, ข้อมูลทางการแพทย์)

#### 4.2 การควบคุมการเข้าถึงข้อมูล (3 ชั่วโมง)
- User, Role, Permission ใน Database
- สร้าง User และกำหนดสิทธิ์ใน MySQL: `GRANT`, `REVOKE`
- Row-Level Security: แสดงข้อมูลตามสิทธิ์ผู้ใช้
- **Workshop:** ออกแบบระบบสิทธิ์สำหรับฐานข้อมูลโรงเรียน (ครู/นักเรียน/ผู้ดูแล)

#### 4.3 การวิเคราะห์ความเสี่ยงของข้อมูล (3 ชั่วโมง)
- ประเภทความเสี่ยง: ความเสี่ยงจากข้อมูล (Data Risk) vs ความเสี่ยงจากการใช้ข้อมูล (Usage Risk)
- Risk Matrix: ความน่าจะเป็น × ผลกระทบ
- การประเมินความเสี่ยง (Risk Assessment) แบบง่าย
- **Workshop:** วิเคราะห์และสรุปความเสี่ยงของระบบข้อมูลสมมติ

#### 4.4 เทคโนโลยีลดความเสี่ยง (2 ชั่วโมง)
- **การเข้ารหัส (Encryption):** Hash Password ด้วย Python `hashlib`
- **การสำรองข้อมูล (Backup):** กลยุทธ์ 3-2-1 Backup
- **Audit Log:** บันทึกการเข้าถึงข้อมูล
- SQL Injection คืออะไร? และป้องกันอย่างไร?
- **Workshop:** สาธิต SQL Injection + วิธีป้องกันด้วย Parameterized Query

---

## หน่วยที่ 5: ข้อมูลไม่มีโครงสร้างและการจัดการข้อมูลหลากหลายรูปแบบ
**เวลา: 10 ชั่วโมง**

### จุดประสงค์
นักเรียนสามารถระบุแหล่งข้อมูล, เข้าถึงข้อมูลหลากหลายรูปแบบ และเลือกเครื่องมือที่เหมาะสมได้

### เนื้อหา

#### 5.1 ประเภทของข้อมูลในโลก Big Data (2 ชั่วโมง)
- **Structured Data:** SQL Table, CSV, Excel
- **Semi-structured Data:** JSON, XML, YAML
- **Unstructured Data:** รูปภาพ, เสียง, วิดีโอ, เอกสาร PDF, ข้อความ Social Media
- แหล่งที่มาและวิธีเข้าถึงข้อมูลแต่ละประเภท

#### 5.2 การจัดการ JSON (3 ชั่วโมง)
- โครงสร้าง JSON: Object, Array, Nested Object
- อ่านและเขียน JSON ด้วย Python: `json.load()`, `json.dump()`
- แปลง JSON → Pandas DataFrame → SQLite
- **Workshop:** ดึงข้อมูล JSON (API สมมติที่ครูเตรียมให้) → บันทึกลงฐานข้อมูล

#### 5.3 NoSQL Database ด้วย MongoDB (3 ชั่วโมง)
- ทำไมต้องใช้ MongoDB? เมื่อไหร่ควรเลือก NoSQL?
- MongoDB Document Model: Collection, Document, Field
- คำสั่งพื้นฐาน: `insertOne`, `find`, `updateOne`, `deleteOne`
- Query แบบมีเงื่อนไข: `$eq`, `$gt`, `$in`, `$and`
- **Workshop:** สร้าง Collection สินค้า + เพิ่ม/ค้นหาข้อมูล

#### 5.4 การเลือกเครื่องมือให้เหมาะกับข้อมูล (2 ชั่วโมง)
- Decision Framework: เมื่อไหร่ใช้ SQL? NoSQL? Python?
- Pipeline ข้อมูลอย่างง่าย (Simple Data Pipeline)
- เตรียมข้อมูลสำหรับ Mini Project (Export เป็น JSON/CSV เพื่อใช้ใน Dashboard)

---

## หน่วยที่ 6: Mini Project — Dashboard ข้อมูลด้วย HTML
**เวลา: 18 ชั่วโมง**

### จุดประสงค์
นักเรียนสามารถออกแบบและสร้าง Dashboard ที่ดึงข้อมูลจากฐานข้อมูลมาแสดงผลผ่านหน้าเว็บ HTML ได้อย่างสมบูรณ์

### เนื้อหา

#### 6.1 สถาปัตยกรรมของ Dashboard (2 ชั่วโมง)
- ภาพรวม: ฐานข้อมูล → Python Backend → JSON → HTML Frontend
- การออกแบบ Dashboard: เลือกข้อมูลอะไรมาแสดง? ทำไม?
- หลักการ Data Visualization เบื้องต้น: กราฟประเภทไหนใช้เมื่อไหร่?
- **Workshop:** วางแผน Dashboard (วาด Wireframe บนกระดาษ)

#### 6.2 สร้าง Backend ด้วย Python Flask (4 ชั่วโมง)
- ติดตั้งและใช้งาน Flask เบื้องต้น
- สร้าง API Endpoint ที่ดึงข้อมูลจาก SQLite
- ส่งข้อมูลเป็น JSON Response
- **ตัวอย่าง Endpoint:**
  - `GET /api/summary` → สรุปข้อมูลรวม
  - `GET /api/students` → รายชื่อนักเรียน
  - `GET /api/scores` → ผลคะแนน

#### 6.3 สร้าง Frontend ด้วย HTML + Chart.js (6 ชั่วโมง)
- โครงสร้าง HTML Dashboard
- ดึงข้อมูลจาก API ด้วย `fetch()` JavaScript
- แสดงผลด้วย **Chart.js** (Bar Chart, Line Chart, Pie Chart, Doughnut)
- สร้างตารางข้อมูลแบบ Dynamic
- การจัด Layout ด้วย CSS Flexbox/Grid
- **Workshop:** สร้าง Dashboard แสดงข้อมูลอย่างน้อย 3 Chart + 1 ตาราง

#### 6.4 เพิ่มฟีเจอร์ขั้นสูง (3 ชั่วโมง)
- Filter ข้อมูล (Dropdown เลือกปี/เดือน/หมวดหมู่)
- Search ข้อมูลในตาราง
- Export ข้อมูลเป็น CSV จากหน้าเว็บ
- Responsive Design (ใช้งานได้บนมือถือ)

#### 6.5 นำเสนอ Mini Project (3 ชั่วโมง)
- แต่ละกลุ่มนำเสนอ Dashboard 10 นาที
- อธิบาย: ข้อมูลมาจากไหน?, SQL ที่ใช้, การตรวจสอบคุณภาพ, ประเด็นความปลอดภัย
- เพื่อนและครูร่วมให้ Feedback

---

## โครงสร้าง Mini Project (งานชิ้นสุดท้าย)

### ข้อกำหนด

```
📁 my_bigdata_project/
├── 📄 README.md              ← อธิบายโปรเจกต์
├── 📄 app.py                 ← Python Flask Backend
├── 📄 school_data.db         ← SQLite Database
├── 📁 static/
│   ├── 📄 style.css
│   └── 📄 chart.js (ดาวน์โหลดไว้ล่วงหน้า)
└── 📁 templates/
    └── 📄 index.html         ← Dashboard หน้าหลัก
```

### เกณฑ์การประเมิน

| หัวข้อ | คะแนน |
|--------|--------|
| ฐานข้อมูล: มีอย่างน้อย 3 ตาราง + ความสัมพันธ์ถูกต้อง | 20 |
| SQL: ใช้ JOIN และ Aggregate Function ได้ | 20 |
| คุณภาพข้อมูล: มีการตรวจสอบและทำความสะอาด | 15 |
| Dashboard: แสดง Chart อย่างน้อย 3 ประเภท | 25 |
| ความปลอดภัย: มีการกำหนดสิทธิ์ / ป้องกัน SQL Injection | 10 |
| การนำเสนอและอธิบาย | 10 |
| **รวม** | **100** |

---

## ตารางการเรียนโดยสรุป

| หน่วย | หัวข้อ | ชั่วโมง | Tool หลัก |
|-------|--------|---------|-----------|
| 1 | พื้นฐาน Big Data & ระบบฐานข้อมูล | 12 | SQLite, DB Browser |
| 2 | SQL สำหรับจัดการข้อมูล | 15 | SQLite, Python sqlite3 |
| 3 | คุณภาพและการตรวจสอบข้อมูล | 10 | Python, Pandas |
| 4 | ความปลอดภัยและความเสี่ยง | 10 | MySQL, Python hashlib |
| 5 | Unstructured Data & NoSQL | 10 | MongoDB, JSON |
| 6 | Mini Project: Dashboard | 18 | Flask, HTML, Chart.js |
| | **รวม** | **75** | |

---

## ไฟล์ที่ครูต้องเตรียมไว้ในแฟลชไดร์ฟ

```
📁 BigData_Course_2026/
├── 📁 software/
│   ├── Python 3.12 Installer (Windows)
│   ├── VS Code Installer
│   ├── DB Browser for SQLite
│   └── MongoDB Community Installer
├── 📁 python_packages/         ← pip install จาก local
│   ├── pandas
│   ├── flask
│   ├── openpyxl
│   └── pymongo
├── 📁 unit01_data/
│   ├── students.csv
│   ├── products.csv
│   └── school_data.db
├── 📁 unit03_dirty_data/       ← ข้อมูลมีปัญหาเจตนา
│   └── dirty_records.csv
├── 📁 unit05_json/
│   └── sample_api_data.json
├── 📁 unit06_project/
│   ├── chart.min.js            ← Chart.js offline
│   ├── app_template.py
│   └── index_template.html
└── 📄 requirements.txt
```

---

*หลักสูตรนี้ออกแบบสำหรับนักเรียนระดับอาชีวศึกษา/มัธยมปลาย ที่มีพื้นฐานคอมพิวเตอร์เบื้องต้น เน้นการปฏิบัติจริง (70% Lab : 30% ทฤษฎี) และสามารถใช้งานได้โดยไม่พึ่งอินเทอร์เน็ต*

