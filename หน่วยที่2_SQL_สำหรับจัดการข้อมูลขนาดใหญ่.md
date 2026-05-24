# หน่วยที่ 2: SQL สำหรับจัดการข้อมูลขนาดใหญ่
### วิชา: การจัดการข้อมูลขนาดใหญ่เบื้องต้น | Introduction to Big Data (พ.ศ. 2026)
**เวลาเรียน: 15 ชั่วโมง** | **เครื่องมือหลัก:** SQLite, DB Browser for SQLite, Python sqlite3

---

## จุดประสงค์การเรียนรู้

เมื่อเรียนจบหน่วยนี้ นักเรียนจะสามารถ:

1. เขียนคำสั่ง DDL สร้าง แก้ไข และลบตารางได้
2. เขียนคำสั่ง DML เพิ่ม แก้ไข และลบข้อมูลได้
3. ค้นหาและกรองข้อมูลด้วย SELECT ขั้นสูงได้
4. เชื่อมตารางหลายตารางด้วย JOIN ได้
5. เชื่อมต่อ SQLite ด้วย Python และส่งออกเป็น CSV/JSON ได้

> **ฐานข้อมูลที่ใช้ตลอดหน่วยนี้:**  
> `road_accidents` — ข้อมูลอุบัติเหตุทางถนนประเทศไทย ปี 2568  
> จำนวน **20,000 records**, **51 columns**, นำเข้าจาก `thailand_road_accidents_2568.csv`

---

# บทที่ 2.1 — คำสั่ง SQL พื้นฐาน: DDL & DML
**(3 ชั่วโมง)**

---

## 🏗️ DDL — Data Definition Language (เดต้า เดฟฟินิชัน แลงกวิจ)

**DDL** คือชุดคำสั่ง SQL ที่ใช้**กำหนดโครงสร้าง**ของฐานข้อมูล ได้แก่ สร้าง แก้ไข และลบตาราง

> **เปรียบเทียบ:** DDL คือการออกแบบและสร้างตึก (โครงสร้าง)  
> ส่วน DML คือการนำของเข้าไปวางในตึก (ข้อมูล)

---

### CREATE TABLE — สร้างตาราง

**รูปแบบ:**
```sql
CREATE TABLE ชื่อตาราง (
    ชื่อคอลัมน์  ประเภทข้อมูล  เงื่อนไข,
    ชื่อคอลัมน์  ประเภทข้อมูล  เงื่อนไข,
    ...
);
```

**ประเภทข้อมูลใน SQLite:**

| ประเภท | ชื่อ | ใช้เก็บ | ตัวอย่าง |
|--------|------|--------|---------|
| `INTEGER` (อินทิเจอร์) | จำนวนเต็ม | อายุ, จำนวน, รหัส | 25, 100, 2568 |
| `TEXT` (เท็กซ์) | ข้อความ | ชื่อ, จังหวัด, สาเหตุ | 'สมชาย', 'กรุงเทพ' |
| `REAL` (เรียล) | ทศนิยม | ละติจูด, ราคา, คะแนน | 13.756, 89.5 |
| `BLOB` (บล็อบ) | ข้อมูลไบนารี | ไฟล์รูป, PDF | (ข้อมูลดิบ) |
| `DATE` (เดท) | วันที่ | วันเกิด, วันเกิดเหตุ | '2568-01-09' |

**เงื่อนไข (Constraints) ที่ใช้บ่อย:**

| เงื่อนไข | ความหมาย |
|---------|---------|
| `PRIMARY KEY` | กำหนดเป็น Primary Key |
| `AUTOINCREMENT` | เพิ่มค่าอัตโนมัติ (1, 2, 3, ...) |
| `NOT NULL` | ห้ามว่าง |
| `UNIQUE` | ห้ามซ้ำกัน |
| `DEFAULT ค่า` | ค่าเริ่มต้นถ้าไม่ได้ใส่ |
| `CHECK (เงื่อนไข)` | ตรวจสอบค่าก่อนบันทึก |

---

**ตัวอย่าง — สร้างตารางจัดการอุบัติเหตุ:**

```sql
-- สร้างตารางจังหวัด (ตารางอ้างอิง)
CREATE TABLE provinces (
    province_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    province_name TEXT    NOT NULL UNIQUE,
    region        TEXT    NOT NULL,
    population    INTEGER DEFAULT 0,
    area_sqkm     INTEGER
);

-- สร้างตารางอุบัติเหตุ
CREATE TABLE accidents (
    accident_id   TEXT    PRIMARY KEY,
    incident_date DATE    NOT NULL,
    incident_time TEXT,
    province_id   INTEGER NOT NULL REFERENCES provinces(province_id),
    vehicle_type  TEXT,
    cause         TEXT,
    severity      TEXT    CHECK(severity IN ('เสียชีวิต','บาดเจ็บสาหัส','บาดเจ็บปานกลาง','บาดเจ็บเล็กน้อย','ไม่บาดเจ็บ')),
    deaths        INTEGER DEFAULT 0 CHECK(deaths >= 0),
    injuries      INTEGER DEFAULT 0 CHECK(injuries >= 0),
    total_cost    INTEGER DEFAULT 0
);
```

> **สังเกต:** `CHECK(severity IN (...))` บังคับให้ค่าในคอลัมน์ severity ต้องเป็นหนึ่งในตัวเลือกเท่านั้น  
> ป้องกันการกรอก "บาดเจ็บมาก" ซึ่งไม่ตรงมาตรฐาน

---

### ALTER TABLE — แก้ไขโครงสร้างตาราง

```sql
-- เพิ่มคอลัมน์ใหม่
ALTER TABLE accidents ADD COLUMN road_type TEXT;

-- เปลี่ยนชื่อตาราง
ALTER TABLE accidents RENAME TO road_accidents_backup;

-- เปลี่ยนชื่อคอลัมน์ (SQLite 3.25.0+)
ALTER TABLE accidents RENAME COLUMN total_cost TO cost_baht;
```

> **หมายเหตุ:** SQLite มีข้อจำกัด ALTER TABLE มากกว่า MySQL  
> ไม่สามารถลบคอลัมน์ด้วย ALTER TABLE ได้ (ต้องสร้างตารางใหม่แทน)

---

### DROP TABLE — ลบตาราง

```sql
-- ลบตาราง (ระวัง! ข้อมูลหายถาวร)
DROP TABLE accidents;

-- ลบแบบปลอดภัย (ไม่ error ถ้าไม่มีตาราง)
DROP TABLE IF EXISTS accidents;
```

> ⚠️ **คำเตือน:** `DROP TABLE` ลบข้อมูลทั้งหมดถาวร ไม่มี Undo — ต้องระวังอย่างมาก!

---

## ✏️ DML — Data Manipulation Language (เดต้า มานิพิวเลชัน แลงกวิจ)

**DML** คือชุดคำสั่งที่ใช้**จัดการข้อมูล**ภายในตาราง ได้แก่ เพิ่ม แก้ไข และลบข้อมูล

---

### INSERT — เพิ่มข้อมูล

**รูปแบบ 1: ระบุคอลัมน์ (แนะนำ)**
```sql
INSERT INTO ชื่อตาราง (คอลัมน์1, คอลัมน์2, ...)
VALUES (ค่า1, ค่า2, ...);
```

**รูปแบบ 2: ใส่ทุกคอลัมน์ตามลำดับ**
```sql
INSERT INTO ชื่อตาราง
VALUES (ค่า1, ค่า2, ...);
```

**ตัวอย่าง — เพิ่มข้อมูลอุบัติเหตุ:**

```sql
-- เพิ่มข้อมูล 1 แถว
INSERT INTO accidents (accident_id, incident_date, province_id, vehicle_type, cause, severity, deaths, injuries)
VALUES ('ACC2568999001', '2568-06-15', 1, 'รถจักรยานยนต์', 'ขับรถเร็วเกินกำหนด', 'บาดเจ็บเล็กน้อย', 0, 1);

-- เพิ่มข้อมูลหลายแถวในคำสั่งเดียว
INSERT INTO provinces (province_name, region, population, area_sqkm) VALUES
    ('กรุงเทพมหานคร', 'ภาคกลาง', 10500000, 1569),
    ('เชียงใหม่',     'ภาคเหนือ', 1800000,  20107),
    ('ขอนแก่น',       'ภาคตะวันออกเฉียงเหนือ', 1800000, 10886),
    ('สงขลา',        'ภาคใต้',   1400000,  7393);
```

---

### UPDATE — แก้ไขข้อมูล

```sql
UPDATE ชื่อตาราง
SET คอลัมน์1 = ค่าใหม่1,
    คอลัมน์2 = ค่าใหม่2
WHERE เงื่อนไข;
```

**ตัวอย่าง:**

```sql
-- แก้ไขค่าใช้จ่ายของอุบัติเหตุที่รหัส ACC2568000001
UPDATE accidents
SET total_cost = 15000
WHERE accident_id = 'ACC2568000001';

-- แก้ไขหลายคอลัมน์พร้อมกัน
UPDATE accidents
SET severity  = 'บาดเจ็บปานกลาง',
    injuries  = 2,
    total_cost = 35000
WHERE accident_id = 'ACC2568000002';
```

> ⚠️ **คำเตือน:** ถ้าลืมใส่ `WHERE` จะแก้ไข**ทุกแถว**ในตาราง!  
> ตัวอย่างอันตราย: `UPDATE accidents SET deaths = 0;` → เปลี่ยนยอดผู้เสียชีวิตทั้งหมดเป็น 0 ทันที

---

### DELETE — ลบข้อมูล

```sql
DELETE FROM ชื่อตาราง
WHERE เงื่อนไข;
```

**ตัวอย่าง:**

```sql
-- ลบอุบัติเหตุที่รหัสนี้
DELETE FROM accidents
WHERE accident_id = 'ACC2568999001';

-- ลบข้อมูลอุบัติเหตุที่ไม่มาดเจ็บและไม่มีค่าใช้จ่าย
DELETE FROM accidents
WHERE severity = 'ไม่บาดเจ็บ' AND total_cost = 0;
```

> ⚠️ **คำเตือน:** ลืม `WHERE` → ลบข้อมูลทั้งหมดในตาราง!  
> แต่ `DELETE FROM accidents;` ยังคงเก็บโครงสร้างตารางไว้ ต่างจาก `DROP TABLE`

---

## 🔧 Workshop 2.1 — สร้างตารางนักเรียนและเพิ่มข้อมูล

```sql
-- ขั้นตอน 1: สร้างตาราง
CREATE TABLE students (
    student_id TEXT    PRIMARY KEY,
    full_name  TEXT    NOT NULL,
    grade      INTEGER CHECK(grade BETWEEN 1 AND 6),
    section    TEXT,
    gpa        REAL    CHECK(gpa BETWEEN 0.0 AND 4.0),
    birthdate  DATE
);

-- ขั้นตอน 2: เพิ่มข้อมูล 5 คน
INSERT INTO students VALUES
    ('STU001', 'สมชาย ใจดี',    4, 'ก', 3.25, '2551-03-15'),
    ('STU002', 'สมหญิง รักเรียน',4, 'ก', 3.80, '2551-07-22'),
    ('STU003', 'วิชัย แกล้วกล้า', 4, 'ข', 2.90, '2551-01-10'),
    ('STU004', 'มาลี สดใส',     4, 'ข', 3.50, '2551-11-05'),
    ('STU005', 'ประเสริฐ เก่งกาจ',4, 'ค', 3.10, '2551-09-30');

-- ขั้นตอน 3: ตรวจสอบ
SELECT * FROM students;

-- ขั้นตอน 4: แก้ไข GPA ของ STU003
UPDATE students SET gpa = 3.00 WHERE student_id = 'STU003';

-- ขั้นตอน 5: ลบนักเรียนที่ GPA ต่ำกว่า 1.0 (ไม่มีในตัวอย่างนี้ แต่ฝึกไว้)
DELETE FROM students WHERE gpa < 1.0;
```

---

# บทที่ 2.2 — การค้นหาข้อมูล: SELECT ขั้นสูง
**(4 ชั่วโมง)**

---

## 🔍 พื้นฐาน SELECT

**รูปแบบครบ:**
```sql
SELECT  คอลัมน์ที่ต้องการ
FROM    ชื่อตาราง
WHERE   เงื่อนไข
GROUP BY คอลัมน์ที่จัดกลุ่ม
HAVING  เงื่อนไขหลังจัดกลุ่ม
ORDER BY คอลัมน์ที่เรียง  ASC/DESC
LIMIT   จำนวนแถว;
```

> **ลำดับการทำงานของ SQL (ไม่ใช่ลำดับที่เขียน!):**  
> `FROM` → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` → `ORDER BY` → `LIMIT`

---

### SELECT, FROM, WHERE

```sql
-- ดูทุกคอลัมน์
SELECT * FROM road_accidents;

-- ดูเฉพาะบางคอลัมน์
SELECT accident_id, วันที่เกิดเหตุ, จังหวัด, ความรุนแรง
FROM road_accidents;

-- กรองด้วย WHERE
SELECT accident_id, จังหวัด, ประเภทยานพาหนะหลัก, จำนวนผู้เสียชีวิต
FROM road_accidents
WHERE จังหวัด = 'เชียงใหม่';
```

---

### ORDER BY — เรียงลำดับ

```sql
-- เรียงจากน้อยไปมาก (ASC = Ascending คือค่าเริ่มต้น)
SELECT accident_id, จังหวัด, ค่าใช้จ่ายรวม_บาท
FROM road_accidents
ORDER BY ค่าใช้จ่ายรวม_บาท ASC;

-- เรียงจากมากไปน้อย (DESC = Descending)
SELECT accident_id, จังหวัด, ค่าใช้จ่ายรวม_บาท
FROM road_accidents
ORDER BY ค่าใช้จ่ายรวม_บาท DESC;

-- เรียงหลายคอลัมน์
SELECT จังหวัด, วันที่เกิดเหตุ, ความรุนแรง
FROM road_accidents
ORDER BY จังหวัด ASC, วันที่เกิดเหตุ DESC;
```

---

### LIMIT — จำกัดจำนวนแถว

```sql
-- ดู 10 อุบัติเหตุแรก
SELECT * FROM road_accidents LIMIT 10;

-- ดู 5 อุบัติเหตุที่มีค่าใช้จ่ายสูงที่สุด
SELECT accident_id, จังหวัด, ค่าใช้จ่ายรวม_บาท
FROM road_accidents
ORDER BY ค่าใช้จ่ายรวม_บาท DESC
LIMIT 5;
```

**ผลลัพธ์ที่คาดว่าจะได้:**
```
accident_id     | จังหวัด    | ค่าใช้จ่ายรวม_บาท
----------------|------------|------------------
ACC2568XXXXXX   | ...        | 2,950,000
ACC2568XXXXXX   | ...        | 2,870,000
...
```

---

## 🔎 เงื่อนไขขั้นสูงใน WHERE

### AND, OR, NOT

```sql
-- AND: ทุกเงื่อนไขต้องเป็นจริง
SELECT accident_id, จังหวัด, ความรุนแรง, ประเภทยานพาหนะหลัก
FROM road_accidents
WHERE จังหวัด = 'กรุงเทพมหานคร'
  AND ความรุนแรง = 'เสียชีวิต';

-- OR: เงื่อนไขใดเงื่อนไขหนึ่งเป็นจริง
SELECT accident_id, จังหวัด, ความรุนแรง
FROM road_accidents
WHERE ความรุนแรง = 'เสียชีวิต'
   OR ความรุนแรง = 'บาดเจ็บสาหัส';

-- NOT: กลับเงื่อนไข
SELECT accident_id, จังหวัด, ประเภทยานพาหนะหลัก
FROM road_accidents
WHERE NOT ประเภทยานพาหนะหลัก = 'รถจักรยานยนต์';
```

---

### BETWEEN — ระหว่างค่าสองค่า

```sql
-- อุบัติเหตุที่มีค่าใช้จ่ายระหว่าง 50,000 - 500,000 บาท
SELECT accident_id, จังหวัด, ค่าใช้จ่ายรวม_บาท
FROM road_accidents
WHERE ค่าใช้จ่ายรวม_บาท BETWEEN 50000 AND 500000;

-- อุบัติเหตุในช่วงเดือนมกราคม - มีนาคม
SELECT accident_id, เดือน, จังหวัด
FROM road_accidents
WHERE เดือน BETWEEN 1 AND 3;
```

> **เทียบเท่ากับ:** `WHERE เดือน >= 1 AND เดือน <= 3`

---

### LIKE — ค้นหาข้อความแบบ Pattern

```sql
-- % = แทนที่ตัวอักษรกี่ตัวก็ได้
-- _ = แทนที่ตัวอักษร 1 ตัวพอดี

-- ค้นหาจังหวัดที่ขึ้นต้นด้วย "เชียง"
SELECT DISTINCT จังหวัด
FROM road_accidents
WHERE จังหวัด LIKE 'เชียง%';
-- ได้: เชียงใหม่, เชียงราย

-- ค้นหาสาเหตุที่มีคำว่า "เร็ว"
SELECT DISTINCT สาเหตุหลักของอุบัติเหตุ
FROM road_accidents
WHERE สาเหตุหลักของอุบัติเหตุ LIKE '%เร็ว%';
-- ได้: ขับรถเร็วเกินกำหนด

-- ค้นหา accident_id ที่ลงท้ายด้วย "001"
SELECT accident_id
FROM road_accidents
WHERE accident_id LIKE '%001';
```

---

### IN — ค่าอยู่ในรายการ

```sql
-- อุบัติเหตุในภาคเหนือ 3 จังหวัด
SELECT accident_id, จังหวัด, ความรุนแรง
FROM road_accidents
WHERE จังหวัด IN ('เชียงใหม่', 'เชียงราย', 'ลำปาง');

-- อุบัติเหตุที่รุนแรงมาก
SELECT accident_id, จังหวัด, ความรุนแรง, จำนวนผู้เสียชีวิต
FROM road_accidents
WHERE ความรุนแรง IN ('เสียชีวิต', 'บาดเจ็บสาหัส')
ORDER BY จำนวนผู้เสียชีวิต DESC;

-- NOT IN: ยกเว้นรายการ
SELECT accident_id, จังหวัด, ภูมิภาค
FROM road_accidents
WHERE ภูมิภาค NOT IN ('ภาคกลาง', 'ภาคตะวันออก');
```

---

### DISTINCT — ค่าที่ไม่ซ้ำกัน

```sql
-- ดูว่ามียานพาหนะประเภทไหนบ้าง (ไม่ซ้ำ)
SELECT DISTINCT ประเภทยานพาหนะหลัก
FROM road_accidents;

-- ดูว่ามีสาเหตุอุบัติเหตุกี่ประเภท
SELECT DISTINCT สาเหตุหลักของอุบัติเหตุ
FROM road_accidents
ORDER BY สาเหตุหลักของอุบัติเหตุ;
```

---

## 📊 Aggregate Functions — ฟังก์ชันสรุปข้อมูล

| ฟังก์ชัน | ชื่อ | ความหมาย | ตัวอย่าง |
|---------|------|---------|---------|
| `COUNT()` (เคาน์ท์) | นับจำนวน | นับจำนวนแถว | `COUNT(*)` = 20,000 |
| `SUM()` (ซัม) | ผลรวม | รวมค่าทั้งหมด | `SUM(จำนวนผู้เสียชีวิต)` = 471 |
| `AVG()` (แอฟเวอเรจ) | ค่าเฉลี่ย | เฉลี่ยทุกแถว | `AVG(ค่าใช้จ่ายรวม_บาท)` |
| `MAX()` (แม็กซ์) | ค่าสูงสุด | หาค่ามากที่สุด | `MAX(อายุ_ปี)` = 85 |
| `MIN()` (มิน) | ค่าต่ำสุด | หาค่าน้อยที่สุด | `MIN(เวลาตอบสนอง_นาที)` = 5 |

**ตัวอย่างการใช้:**

```sql
-- สถิติภาพรวมอุบัติเหตุทั้งหมด
SELECT 
    COUNT(*)                           AS จำนวนอุบัติเหตุ,
    SUM(จำนวนผู้เสียชีวิต)             AS รวมเสียชีวิต,
    SUM(จำนวนผู้บาดเจ็บ)              AS รวมบาดเจ็บ,
    ROUND(AVG(ค่าใช้จ่ายรวม_บาท), 0)  AS คชจ_เฉลี่ย_บาท,
    MAX(ค่าใช้จ่ายรวม_บาท)            AS คชจ_สูงสุด_บาท,
    ROUND(AVG(อายุ_ปี), 1)            AS อายุเฉลี่ย_ผู้ขับ
FROM road_accidents;
```

**ผลลัพธ์ที่คาดว่าจะได้:**
```
จำนวนอุบัติเหตุ | รวมเสียชีวิต | รวมบาดเจ็บ | คชจ_เฉลี่ย_บาท | คชจ_สูงสุด_บาท | อายุเฉลี่ย_ผู้ขับ
20000           | 471          | 20573      | 56,300         | 3,000,000      | 37.5
```

---

## 📦 GROUP BY และ HAVING

### GROUP BY — จัดกลุ่มข้อมูล

```sql
-- นับอุบัติเหตุแยกตามจังหวัด
SELECT จังหวัด, COUNT(*) AS จำนวนเหตุ
FROM road_accidents
GROUP BY จังหวัด
ORDER BY จำนวนเหตุ DESC;

-- สรุปข้อมูลแยกตามยานพาหนะ
SELECT 
    ประเภทยานพาหนะหลัก,
    COUNT(*)                      AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต)        AS รวมเสียชีวิต,
    ROUND(AVG(ค่าใช้จ่ายรวม_บาท), 0) AS คชจ_เฉลี่ย
FROM road_accidents
GROUP BY ประเภทยานพาหนะหลัก
ORDER BY จำนวนเหตุ DESC;
```

**ผลลัพธ์ที่คาดว่าจะได้:**
```
ประเภทยานพาหนะหลัก    | จำนวนเหตุ | รวมเสียชีวิต | คชจ_เฉลี่ย
รถจักรยานยนต์          | 14,400    | 280          | 48,000
รถยนต์ส่วนบุคคล       | 2,800     | 85           | 72,000
รถปิกอัพ/กระบะ        | 1,400     | 55           | 95,000
...
```

---

### HAVING — กรองหลังจัด GROUP

```sql
-- WHERE กรองก่อน GROUP BY  
-- HAVING กรองหลัง GROUP BY

-- หาจังหวัดที่มีอุบัติเหตุมากกว่า 400 ครั้ง
SELECT จังหวัด, COUNT(*) AS จำนวนเหตุ
FROM road_accidents
GROUP BY จังหวัด
HAVING COUNT(*) > 400
ORDER BY จำนวนเหตุ DESC;

-- หาสาเหตุที่ทำให้มีผู้เสียชีวิตรวมมากกว่า 30 ราย
SELECT 
    สาเหตุหลักของอุบัติเหตุ,
    COUNT(*)                   AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต)     AS รวมเสียชีวิต
FROM road_accidents
GROUP BY สาเหตุหลักของอุบัติเหตุ
HAVING SUM(จำนวนผู้เสียชีวิต) > 30
ORDER BY รวมเสียชีวิต DESC;
```

> **ความต่างระหว่าง WHERE และ HAVING:**

```
SELECT จังหวัด, COUNT(*) AS จำนวน
FROM road_accidents
WHERE เดือน = 1               ← WHERE: กรองแถวก่อน GROUP BY (เดือน 1 เท่านั้น)
GROUP BY จังหวัด
HAVING COUNT(*) > 50;          ← HAVING: กรองหลัง GROUP BY (เฉพาะกลุ่มที่มีเหตุ > 50 ครั้ง)
```

---

## 🔧 Workshop 2.2 — วิเคราะห์อุบัติเหตุทางถนน

```sql
-- โจทย์ 1: Top 5 สาเหตุที่เกิดบ่อยที่สุด
SELECT สาเหตุหลักของอุบัติเหตุ, COUNT(*) AS จำนวน
FROM road_accidents
GROUP BY สาเหตุหลักของอุบัติเหตุ
ORDER BY จำนวน DESC
LIMIT 5;

-- โจทย์ 2: อุบัติเหตุในช่วงกลางคืน เสียชีวิตสูงสุด
SELECT จังหวัด, COUNT(*) AS จำนวน, SUM(จำนวนผู้เสียชีวิต) AS เสียชีวิต
FROM road_accidents
WHERE ช่วงเวลากลางวัน_กลางคืน = 'กลางคืน'
GROUP BY จังหวัด
HAVING SUM(จำนวนผู้เสียชีวิต) > 0
ORDER BY เสียชีวิต DESC
LIMIT 10;

-- โจทย์ 3: เปรียบเทียบวันหยุด vs วันปกติ
SELECT 
    วันหยุด_วันปกติ,
    COUNT(*)                  AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต)    AS รวมเสียชีวิต,
    ROUND(AVG(ค่าใช้จ่ายรวม_บาท),0) AS คชจ_เฉลี่ย
FROM road_accidents
GROUP BY วันหยุด_วันปกติ;
```

---

# บทที่ 2.3 — การเชื่อมตาราง: JOIN
**(4 ชั่วโมง)**

---

## 🔗 ทำไมต้องใช้ JOIN?

ในฐานข้อมูลจริง ข้อมูลไม่ได้อยู่ในตารางเดียว เราออกแบบหลายตารางเพื่อลดการซ้ำซ้อน แต่เวลาจะดูข้อมูลครบ ต้อง "เชื่อม" ตารางหลาย ๆ ตารางเข้าหากัน

**สถานการณ์ตัวอย่าง — ระบบโรงเรียน:**

```
ตาราง students:          ตาราง enrollments:        ตาราง subjects:
┌────────┬────────┐      ┌────────┬─────────┬──────┐  ┌─────────┬───────────┐
│std_id  │name    │      │enr_id  │std_id 🔗│score │  │subj_id  │subj_name  │
├────────┼────────┤      ├────────┼─────────┼──────┤  ├─────────┼───────────┤
│STU001  │สมชาย  │      │ENR001  │STU001   │  85  │  │MAT101   │คณิตศาสตร์ │
│STU002  │สมหญิง │      │ENR002  │STU001   │  72  │  │ENG101   │ภาษาอังกฤษ │
└────────┴────────┘      │ENR003  │STU002   │  91  │  └─────────┴───────────┘
                         └────────┴─────────┴──────┘
```

ถ้าต้องการ "ชื่อนักเรียน + วิชา + คะแนน" ต้องเชื่อม 3 ตารางด้วย JOIN

---

## INNER JOIN — เอาเฉพาะที่ตรงกัน

**ความหมาย:** เอาเฉพาะแถวที่มีข้อมูลตรงกันใน**ทั้งสองตาราง**

```sql
SELECT ตารางA.คอลัมน์, ตารางB.คอลัมน์
FROM ตารางA
INNER JOIN ตารางB ON ตารางA.คีย์ = ตารางB.คีย์;
```

**ตัวอย่าง — เชื่อมนักเรียนกับผลการเรียน:**

```sql
SELECT s.std_id, s.name, e.subj_id, e.score
FROM students s
INNER JOIN enrollments e ON s.std_id = e.std_id;
```

**ผลลัพธ์:**
```
std_id | name   | subj_id | score
-------|--------|---------|------
STU001 | สมชาย  | MAT101  | 85
STU001 | สมชาย  | ENG101  | 72
STU002 | สมหญิง | MAT101  | 91
```

> แถวที่ไม่มีคู่ในอีกตาราง จะ**ไม่ปรากฏ**ในผลลัพธ์

**ตัวอย่างกับข้อมูลอุบัติเหตุ — เชื่อมกับตารางจังหวัด:**

```sql
-- สมมติมีตาราง provinces แยกต่างหาก
SELECT 
    a.accident_id,
    a.วันที่เกิดเหตุ,
    p.province_name,
    p.region,
    a.ประเภทยานพาหนะหลัก,
    a.ความรุนแรง
FROM accidents a
INNER JOIN provinces p ON a.province_id = p.province_id
WHERE p.region = 'ภาคเหนือ'
ORDER BY a.วันที่เกิดเหตุ;
```

---

## LEFT JOIN — เอาทุกแถวจากตารางซ้าย

**ความหมาย:** เอา**ทุกแถวจากตารางซ้าย (LEFT)** และแถวที่ตรงกันจากตารางขวา ถ้าไม่มีคู่ → แสดง NULL

```sql
SELECT s.std_id, s.name, e.score
FROM students s
LEFT JOIN enrollments e ON s.std_id = e.std_id;
```

**ผลลัพธ์ (สมมติ STU003 ยังไม่ได้ลงทะเบียน):**
```
std_id | name    | score
-------|---------|------
STU001 | สมชาย   | 85
STU001 | สมชาย   | 72
STU002 | สมหญิง  | 91
STU003 | วิชัย   | NULL  ← ไม่มีการลงทะเบียน แต่ยังแสดงนักเรียน
```

> **ใช้เมื่อ:** ต้องการเห็นทุกรายการในตารางหลัก แม้ว่าจะไม่มีข้อมูลในตารางรอง

---

## RIGHT JOIN — เอาทุกแถวจากตารางขวา

**ความหมาย:** ตรงข้ามกับ LEFT JOIN — เอา**ทุกแถวจากตารางขวา (RIGHT)**

> **หมายเหตุ:** SQLite ไม่รองรับ RIGHT JOIN โดยตรง  
> วิธีแก้: สลับลำดับตารางแล้วใช้ LEFT JOIN แทน

```sql
-- แทน RIGHT JOIN ใน SQLite
-- เดิม: FROM tableA RIGHT JOIN tableB
-- แก้เป็น:
SELECT * FROM enrollments e
LEFT JOIN students s ON e.std_id = s.std_id;
```

---

## การ JOIN หลายตาราง

```sql
-- ดึงชื่อนักเรียน + ชื่อวิชา + คะแนน (3 ตาราง)
SELECT 
    s.name          AS ชื่อนักเรียน,
    sub.subj_name   AS ชื่อวิชา,
    e.score         AS คะแนน
FROM students s
INNER JOIN enrollments e   ON s.std_id    = e.std_id
INNER JOIN subjects    sub ON e.subj_id   = sub.subj_id
ORDER BY s.name, e.score DESC;
```

**ผลลัพธ์:**
```
ชื่อนักเรียน | ชื่อวิชา     | คะแนน
------------|-------------|------
สมชาย       | คณิตศาสตร์  | 85
สมชาย       | ภาษาอังกฤษ  | 72
สมหญิง      | คณิตศาสตร์  | 91
```

---

## Subquery — คำสั่งซ้อนใน SQL

**Subquery** (ซับควีรี่) คือ คำสั่ง SELECT ที่ซ้อนอยู่ใน SELECT อื่น ใช้เมื่อต้องการนำผลลัพธ์ของ Query หนึ่งมาใช้ใน Query อีกอัน

### Subquery ใน WHERE

```sql
-- หาอุบัติเหตุที่มีค่าใช้จ่ายสูงกว่าค่าเฉลี่ย
SELECT accident_id, จังหวัด, ค่าใช้จ่ายรวม_บาท
FROM road_accidents
WHERE ค่าใช้จ่ายรวม_บาท > (
    SELECT AVG(ค่าใช้จ่ายรวม_บาท) FROM road_accidents
)
ORDER BY ค่าใช้จ่ายรวม_บาท DESC
LIMIT 10;
```

### Subquery ใน FROM

```sql
-- หาจังหวัดที่มีอุบัติเหตุสูงกว่าค่าเฉลี่ยของทุกจังหวัด
SELECT จังหวัด, จำนวนเหตุ
FROM (
    SELECT จังหวัด, COUNT(*) AS จำนวนเหตุ
    FROM road_accidents
    GROUP BY จังหวัด
) AS province_summary
WHERE จำนวนเหตุ > (
    SELECT AVG(cnt) FROM (
        SELECT COUNT(*) AS cnt
        FROM road_accidents
        GROUP BY จังหวัด
    )
)
ORDER BY จำนวนเหตุ DESC;
```

---

## 🔧 Workshop 2.3 — ดึงข้อมูลนักเรียน + ผลการเรียน + รายวิชา

```sql
-- สร้างตารางระบบโรงเรียน
CREATE TABLE subjects (
    subj_id   TEXT PRIMARY KEY,
    subj_name TEXT NOT NULL,
    credits   INTEGER DEFAULT 1,
    teacher   TEXT
);

CREATE TABLE enrollments (
    enr_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    std_id    TEXT REFERENCES students(student_id),
    subj_id   TEXT REFERENCES subjects(subj_id),
    score     REAL,
    semester  TEXT
);

-- เพิ่มข้อมูลวิชา
INSERT INTO subjects VALUES
    ('MAT101', 'คณิตศาสตร์', 3, 'ครูสมศักดิ์'),
    ('ENG101', 'ภาษาอังกฤษ', 3, 'ครูสมบัติ'),
    ('SCI101', 'วิทยาศาสตร์', 3, 'ครูสมหวัง'),
    ('THA101', 'ภาษาไทย',    2, 'ครูสมใจ');

-- เพิ่มผลการเรียน
INSERT INTO enrollments (std_id, subj_id, score, semester) VALUES
    ('STU001', 'MAT101', 85.0, '2567/1'),
    ('STU001', 'ENG101', 72.0, '2567/1'),
    ('STU002', 'MAT101', 91.0, '2567/1'),
    ('STU002', 'SCI101', 88.0, '2567/1'),
    ('STU003', 'THA101', 76.0, '2567/1');

-- ดึงข้อมูลครบจาก 3 ตาราง
SELECT 
    s.student_id    AS รหัสนักเรียน,
    s.full_name     AS ชื่อ,
    sub.subj_name   AS วิชา,
    sub.teacher     AS ครูผู้สอน,
    e.score         AS คะแนน,
    CASE 
        WHEN e.score >= 80 THEN 'A'
        WHEN e.score >= 70 THEN 'B'
        WHEN e.score >= 60 THEN 'C'
        ELSE 'F'
    END AS เกรด
FROM students s
INNER JOIN enrollments e   ON s.student_id = e.std_id
INNER JOIN subjects    sub ON e.subj_id    = sub.subj_id
ORDER BY s.student_id, e.score DESC;
```

---

# บทที่ 2.4 — View, Index และ Transaction
**(2 ชั่วโมง)**

---

## 👁️ VIEW — มุมมองข้อมูลเสมือน

**VIEW** (วิว) คือ **ตารางเสมือน** ที่สร้างจากคำสั่ง SELECT — ไม่ได้เก็บข้อมูลจริง แต่ดึงข้อมูลสดจากตารางต้นทางทุกครั้งที่เรียกใช้

**ประโยชน์ของ VIEW:**
- บันทึก Query ที่ซับซ้อนไว้ใช้ซ้ำได้
- ซ่อนคอลัมน์ที่ไม่ต้องการให้ผู้ใช้เห็น
- ทำให้ Query ง่ายขึ้น

```sql
-- สร้าง VIEW สรุปอุบัติเหตุรายจังหวัด
CREATE VIEW v_province_summary AS
SELECT 
    จังหวัด,
    ภูมิภาค,
    COUNT(*)                           AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต)              AS รวมเสียชีวิต,
    SUM(จำนวนผู้บาดเจ็บ)               AS รวมบาดเจ็บ,
    ROUND(AVG(ค่าใช้จ่ายรวม_บาท), 0)   AS คชจ_เฉลี่ย,
    SUM(ค่าใช้จ่ายรวม_บาท)             AS คชจ_รวม
FROM road_accidents
GROUP BY จังหวัด, ภูมิภาค;

-- ใช้งาน VIEW เหมือนตารางปกติ
SELECT * FROM v_province_summary
WHERE ภูมิภาค = 'ภาคเหนือ'
ORDER BY จำนวนเหตุ DESC;

-- ลบ VIEW
DROP VIEW IF EXISTS v_province_summary;
```

> **เปรียบเทียบ:** VIEW คือ "ทางลัด" — เหมือนบันทึก Query ไว้ใช้ซ้ำโดยไม่ต้องพิมพ์ใหม่ทุกครั้ง

---

## ⚡ INDEX — ดัชนีช่วยค้นหาเร็ว

**INDEX** (อินเด็กซ์) คือโครงสร้างข้อมูลพิเศษที่ช่วยให้ SQL ค้นหาข้อมูลได้เร็วขึ้นมาก

**เปรียบเทียบ:** INDEX เหมือนดัชนีหนังสือ  
แทนที่จะพลิกทุกหน้าเพื่อหา "빅데이터" → ดูดัชนีหลังเล่มเจอทันทีที่หน้า 45

```sql
-- สร้าง INDEX บนคอลัมน์จังหวัด (ค้นหาตามจังหวัดจะเร็วขึ้น)
CREATE INDEX idx_province ON road_accidents(จังหวัด);

-- สร้าง INDEX บนหลายคอลัมน์ (Composite Index)
CREATE INDEX idx_province_date ON road_accidents(จังหวัด, วันที่เกิดเหตุ);

-- ดู INDEX ทั้งหมดในตาราง
PRAGMA index_list(road_accidents);

-- ลบ INDEX
DROP INDEX IF EXISTS idx_province;
```

**เมื่อไหร่ควรสร้าง INDEX:**

| ควรสร้าง | ไม่ควรสร้าง |
|---------|----------|
| คอลัมน์ที่ใช้ใน WHERE บ่อย | ตารางที่มีข้อมูลน้อย (<1,000 แถว) |
| คอลัมน์ที่ใช้ JOIN | คอลัมน์ที่ UPDATE บ่อยมาก |
| คอลัมน์ที่ใช้ ORDER BY | คอลัมน์ที่ค่าซ้ำกันมาก (เช่น เพศ ม/ญ) |

---

## 🔒 TRANSACTION — ทำงานแบบกลุ่ม

**TRANSACTION** (แทรนแซกชัน) คือ กลุ่มคำสั่ง SQL ที่ต้องสำเร็จ**ทั้งหมด** หรือ**ยกเลิกทั้งหมด** — ไม่มีทำครึ่ง ๆ กลาง ๆ

**คำสั่งใน TRANSACTION:**

| คำสั่ง | ความหมาย |
|-------|---------|
| `BEGIN` (บีกิน) | เริ่มต้น Transaction |
| `COMMIT` (คอมมิท) | ยืนยัน — บันทึกทุกการเปลี่ยนแปลง |
| `ROLLBACK` (โรลแบ็ค) | ยกเลิก — คืนกลับสู่สภาพก่อนเริ่ม |

**ตัวอย่าง — โอนเงินระหว่างบัญชี:**

```sql
BEGIN;

-- ขั้นตอน 1: หักเงินจากบัญชีต้นทาง
UPDATE bank_accounts
SET balance = balance - 5000
WHERE account_id = 'ACC001';

-- ขั้นตอน 2: เพิ่มเงินในบัญชีปลายทาง
UPDATE bank_accounts
SET balance = balance + 5000
WHERE account_id = 'ACC002';

-- ถ้าทุกอย่างถูกต้อง → บันทึก
COMMIT;

-- ถ้ามีข้อผิดพลาด → ยกเลิกทั้งหมด (ใช้ใน error handling)
-- ROLLBACK;
```

> **ถ้าไม่มี TRANSACTION:** ถ้าไฟดับหลังหักเงิน ACC001 แต่ก่อนเพิ่มให้ ACC002  
> → เงิน 5,000 บาทหายไปจากระบบ! TRANSACTION ป้องกันปัญหานี้

**ตัวอย่าง TRANSACTION กับข้อมูลอุบัติเหตุ:**

```sql
BEGIN;

-- เพิ่มข้อมูลอุบัติเหตุใหม่พร้อมกัน
INSERT INTO accidents (accident_id, incident_date, province_id, vehicle_type, severity)
VALUES ('ACC2568999999', '2568-12-31', 1, 'รถจักรยานยนต์', 'บาดเจ็บเล็กน้อย');

-- อัปเดตสถิติรายจังหวัด
UPDATE province_stats
SET total_accidents = total_accidents + 1
WHERE province_id = 1;

COMMIT;
```

---

# บทที่ 2.5 — เชื่อมต่อฐานข้อมูลด้วย Python
**(2 ชั่วโมง)**

---

## 🐍 เชื่อมต่อ SQLite ด้วย Python

Python มี library ชื่อ `sqlite3` ติดมาพร้อมกันโดยไม่ต้องติดตั้งเพิ่ม

**โครงสร้างพื้นฐาน:**

```python
import sqlite3

# 1. เชื่อมต่อฐานข้อมูล (สร้างใหม่ถ้าไม่มี)
conn = sqlite3.connect('road_accidents.db')

# 2. สร้าง cursor สำหรับรัน SQL
cursor = conn.cursor()

# 3. รันคำสั่ง SQL
cursor.execute("SELECT * FROM road_accidents LIMIT 5")

# 4. ดึงผลลัพธ์
rows = cursor.fetchall()
for row in rows:
    print(row)

# 5. ปิดการเชื่อมต่อ (สำคัญมาก!)
conn.close()
```

---

## 📊 ดึงข้อมูลเข้า Pandas DataFrame

**Pandas** (แพนด้าส) เป็น library Python สำหรับวิเคราะห์ข้อมูล โดยเก็บในรูปแบบ **DataFrame** (เดต้าเฟรม) ซึ่งคล้ายตาราง Excel

```python
import sqlite3
import pandas as pd

# เชื่อมต่อและดึงข้อมูลเข้า DataFrame ในคำสั่งเดียว
conn = sqlite3.connect('road_accidents.db')

# ดึงข้อมูลทั้งตาราง
df = pd.read_sql_query("SELECT * FROM road_accidents", conn)

# ดูข้อมูลเบื้องต้น
print(df.shape)          # (20000, 51) — จำนวนแถว x คอลัมน์
print(df.head())         # 5 แถวแรก
print(df.dtypes)         # ประเภทข้อมูลแต่ละคอลัมน์
print(df.describe())     # สถิติเบื้องต้น (mean, min, max, ...)

conn.close()
```

---

## 🔍 วิเคราะห์ข้อมูลด้วย Python + SQL

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('road_accidents.db')

# Query 1: สรุปอุบัติเหตุรายจังหวัด
query_province = """
SELECT 
    จังหวัด,
    ภูมิภาค,
    COUNT(*) AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต) AS รวมเสียชีวิต,
    ROUND(AVG(ค่าใช้จ่ายรวม_บาท), 0) AS คชจ_เฉลี่ย
FROM road_accidents
GROUP BY จังหวัด, ภูมิภาค
ORDER BY จำนวนเหตุ DESC
LIMIT 10
"""
df_province = pd.read_sql_query(query_province, conn)
print("Top 10 จังหวัดที่เกิดอุบัติเหตุมากที่สุด:")
print(df_province)

# Query 2: อุบัติเหตุรายเดือน
query_monthly = """
SELECT 
    เดือน,
    COUNT(*) AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต) AS รวมเสียชีวิต
FROM road_accidents
GROUP BY เดือน
ORDER BY เดือน
"""
df_monthly = pd.read_sql_query(query_monthly, conn)

# Query 3: สาเหตุหลัก Top 5
query_cause = """
SELECT สาเหตุหลักของอุบัติเหตุ, COUNT(*) AS จำนวน
FROM road_accidents
GROUP BY สาเหตุหลักของอุบัติเหตุ
ORDER BY จำนวน DESC
LIMIT 5
"""
df_cause = pd.read_sql_query(query_cause, conn)

conn.close()
print("\nTop 5 สาเหตุอุบัติเหตุ:")
print(df_cause)
```

---

## 💾 Export ผลลัพธ์เป็น CSV และ JSON

```python
import sqlite3
import pandas as pd
import json

conn = sqlite3.connect('road_accidents.db')

# ดึงข้อมูลสรุปรายจังหวัด
query = """
SELECT 
    จังหวัด, ภูมิภาค,
    COUNT(*) AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต) AS รวมเสียชีวิต,
    SUM(จำนวนผู้บาดเจ็บ) AS รวมบาดเจ็บ,
    ROUND(SUM(ค่าใช้จ่ายรวม_บาท)/1000000.0, 2) AS คชจ_รวม_ล้านบาท
FROM road_accidents
GROUP BY จังหวัด, ภูมิภาค
ORDER BY จำนวนเหตุ DESC
"""
df = pd.read_sql_query(query, conn)
conn.close()

# Export เป็น CSV (สำหรับ Excel / แชร์ให้ทีม)
df.to_csv('province_summary.csv', index=False, encoding='utf-8-sig')
print("✅ บันทึก province_summary.csv สำเร็จ")

# Export เป็น JSON (สำหรับใช้ใน Dashboard / JavaScript)
df.to_json('province_summary.json', orient='records', force_ascii=False, indent=2)
print("✅ บันทึก province_summary.json สำเร็จ")

# ดูตัวอย่าง JSON ที่ได้
with open('province_summary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
print(f"\nจำนวนจังหวัดในไฟล์ JSON: {len(data)}")
print("ตัวอย่าง 2 รายการแรก:")
print(json.dumps(data[:2], ensure_ascii=False, indent=2))
```

**ตัวอย่างไฟล์ JSON ที่ได้:**
```json
[
  {
    "จังหวัด": "กรุงเทพมหานคร",
    "ภูมิภาค": "ภาคกลาง",
    "จำนวนเหตุ": 520,
    "รวมเสียชีวิต": 12,
    "รวมบาดเจ็บ": 538,
    "คชจ_รวม_ล้านบาท": 28.5
  },
  ...
]
```

> ไฟล์ JSON นี้พร้อมใช้ใน **หน่วยที่ 6: Dashboard HTML** โดยตรง!

---

## 🔧 Workshop 2.5 — Pipeline ข้อมูลอุบัติเหตุ

```python
"""
Workshop: Python Data Pipeline
1. ดึงข้อมูลจาก SQLite
2. วิเคราะห์ด้วย Pandas
3. Export เป็น CSV และ JSON
"""

import sqlite3
import pandas as pd

# ── STEP 1: เชื่อมต่อ SQLite ────────────────────────────
conn = sqlite3.connect('road_accidents.db')
print("✅ เชื่อมต่อ SQLite สำเร็จ")

# ── STEP 2: ดึงข้อมูลทั้งหมด ────────────────────────────
df = pd.read_sql_query("SELECT * FROM road_accidents", conn)
print(f"✅ ดึงข้อมูลสำเร็จ: {df.shape[0]:,} แถว, {df.shape[1]} คอลัมน์")

# ── STEP 3: วิเคราะห์เบื้องต้น ──────────────────────────
print("\n📊 สถิติภาพรวม:")
print(f"   รวมเสียชีวิต : {df['จำนวนผู้เสียชีวิต'].sum():,} ราย")
print(f"   รวมบาดเจ็บ  : {df['จำนวนผู้บาดเจ็บ'].sum():,} ราย")
print(f"   คชจ เฉลี่ย  : {df['ค่าใช้จ่ายรวม_บาท'].mean():,.0f} บาท")

print("\n🏍️ ยานพาหนะที่เกิดเหตุมากที่สุด:")
print(df['ประเภทยานพาหนะหลัก'].value_counts().head())

print("\n📅 เดือนที่เกิดอุบัติเหตุมากที่สุด:")
print(df['เดือน'].value_counts().sort_index())

# ── STEP 4: Export ──────────────────────────────────────
df.to_csv('accidents_clean.csv', index=False, encoding='utf-8-sig')
print("\n✅ Export accidents_clean.csv สำเร็จ")

summary = df.groupby('จังหวัด').agg(
    จำนวนเหตุ=('accident_id', 'count'),
    รวมเสียชีวิต=('จำนวนผู้เสียชีวิต', 'sum'),
).reset_index()
summary.to_json('summary_by_province.json', orient='records', force_ascii=False, indent=2)
print("✅ Export summary_by_province.json สำเร็จ")

conn.close()
print("\n✅ ปิดการเชื่อมต่อสำเร็จ — Pipeline เสร็จสมบูรณ์!")
```


---

## 🔗 เชื่อมโยงสู่หน่วยถัดไป

หลังเรียนหน่วยที่ 2 เราจะเข้าสู่ **หน่วยที่ 3: คุณภาพข้อมูลและการตรวจสอบ** (10 ชั่วโมง)  
โดยใช้ SQL ที่เพิ่งเรียนมา ค้นหาปัญหา เช่น NULL, ค่าซ้ำ, รูปแบบผิด  
และใช้ Python + Pandas ทำความสะอาดข้อมูลชุดอุบัติเหตุอย่างเป็นระบบ

```
หน่วยที่ 1 ✅ → หน่วยที่ 2 ✅ → หน่วยที่ 3 (Data Quality) → หน่วยที่ 4 → ...
```

---

## 📌 สรุปคำสั่ง SQL หน่วยที่ 2 (Quick Reference)

```sql
-- DDL
CREATE TABLE t (col TYPE CONSTRAINT, ...);
ALTER TABLE t ADD COLUMN col TYPE;
DROP TABLE IF EXISTS t;

-- DML
INSERT INTO t (col1, col2) VALUES (v1, v2);
UPDATE t SET col = val WHERE condition;
DELETE FROM t WHERE condition;

-- SELECT
SELECT col FROM t WHERE cond ORDER BY col DESC LIMIT n;
SELECT col FROM t WHERE col BETWEEN a AND b;
SELECT col FROM t WHERE col LIKE 'pattern%';
SELECT col FROM t WHERE col IN ('a', 'b', 'c');
SELECT DISTINCT col FROM t;

-- Aggregate
SELECT COUNT(*), SUM(col), AVG(col), MAX(col), MIN(col) FROM t;
SELECT col, COUNT(*) FROM t GROUP BY col HAVING COUNT(*) > n;

-- JOIN
SELECT ... FROM t1 INNER JOIN t2 ON t1.id = t2.id;
SELECT ... FROM t1 LEFT JOIN t2 ON t1.id = t2.id;

-- VIEW & INDEX
CREATE VIEW v AS SELECT ...;
CREATE INDEX idx ON t(col);

-- TRANSACTION
BEGIN; ... COMMIT;
BEGIN; ... ROLLBACK;

-- Python
conn = sqlite3.connect('db.db')
df = pd.read_sql_query("SELECT ...", conn)
df.to_csv('file.csv', index=False, encoding='utf-8-sig')
df.to_json('file.json', orient='records', force_ascii=False)
```

---

*เอกสารนี้จัดทำสำหรับหลักสูตร "การจัดการข้อมูลขนาดใหญ่เบื้องต้น" พ.ศ. 2026*  
*ข้อมูลตัวอย่างอ้างอิงจาก `thailand_road_accidents_2568.csv` — ข้อมูลสังเคราะห์เพื่อการศึกษา*
