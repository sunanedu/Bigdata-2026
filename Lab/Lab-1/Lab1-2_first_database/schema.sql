-- Lab 1.2: ฐานข้อมูลแรก (Workshop 1.2)
-- ตาราง students ตามเอกสารหน่วยที่ 1

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    name  TEXT    NOT NULL,
    grade INTEGER,
    score REAL
);
