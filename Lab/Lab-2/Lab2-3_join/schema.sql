-- Lab 2.3 — ระบบโรงเรียนสำหรับ JOIN (Workshop 2.3)

DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id TEXT    PRIMARY KEY,
    full_name  TEXT    NOT NULL,
    grade      INTEGER CHECK(grade BETWEEN 1 AND 6),
    section    TEXT,
    gpa        REAL    CHECK(gpa BETWEEN 0.0 AND 4.0),
    birthdate  DATE
);

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
