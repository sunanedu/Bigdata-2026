-- Workshop 2.1 — DDL & DML (บทที่ 2.1)
-- เปิดไฟล์นี้กับ output/ddl_students.db ใน DB Browser

-- ขั้นตอน 1: สร้างตาราง
DROP TABLE IF EXISTS students;

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
    ('STU001', 'สมชาย ใจดี',      4, 'ก', 3.25, '2551-03-15'),
    ('STU002', 'สมหญิง รักเรียน',  4, 'ก', 3.80, '2551-07-22'),
    ('STU003', 'วิชัย แกล้วกล้า',  4, 'ข', 2.90, '2551-01-10'),
    ('STU004', 'มาลี สดใส',       4, 'ข', 3.50, '2551-11-05'),
    ('STU005', 'ประเสริฐ เก่งกาจ', 4, 'ค', 3.10, '2551-09-30');

-- ขั้นตอน 3: ตรวจสอบ
SELECT * FROM students;

-- ขั้นตอน 4: แก้ไข GPA ของ STU003
UPDATE students SET gpa = 3.00 WHERE student_id = 'STU003';

-- ขั้นตอน 5: ลบนักเรียนที่ GPA ต่ำกว่า 1.0
DELETE FROM students WHERE gpa < 1.0;
