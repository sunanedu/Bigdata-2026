-- SQLite: โครงสร้างระบบโรงเรียนสำหรับ Lab 4.2
-- (SQLite ไม่มี GRANT — ใช้ร่วมกับ access_control.py และ VIEW)

DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS schedule;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS subjects;

CREATE TABLE users (
    user_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt       TEXT NOT NULL,
    role       TEXT NOT NULL CHECK(role IN ('admin', 'teacher', 'student', 'parent'))
);

CREATE TABLE students (
    student_id TEXT PRIMARY KEY,
    full_name  TEXT NOT NULL,
    grade_level INTEGER,
    parent_username TEXT
);

CREATE TABLE teachers (
    teacher_id TEXT PRIMARY KEY,
    full_name  TEXT NOT NULL,
    salary     REAL,
    phone      TEXT
);

CREATE TABLE subjects (
    subject_id   TEXT PRIMARY KEY,
    subject_name TEXT NOT NULL,
    credits      INTEGER
);

CREATE TABLE grades (
    grade_id   TEXT PRIMARY KEY,
    student_id TEXT NOT NULL REFERENCES students(student_id),
    subject_id TEXT NOT NULL REFERENCES subjects(subject_id),
    score      REAL,
    semester   TEXT
);

CREATE TABLE schedule (
    schedule_id TEXT PRIMARY KEY,
    subject_id  TEXT NOT NULL REFERENCES subjects(subject_id),
    day_of_week TEXT,
    period      INTEGER
);

CREATE TABLE audit_log (
    log_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp  TEXT DEFAULT (datetime('now', 'localtime')),
    username   TEXT NOT NULL,
    action     TEXT NOT NULL,
    table_name TEXT,
    record_id  TEXT,
    old_value  TEXT,
    new_value  TEXT,
    ip_address TEXT,
    status     TEXT DEFAULT 'SUCCESS'
);
