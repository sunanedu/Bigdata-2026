-- Lab 2.1 — เฉลยแบบฝึก (ครูใช้ตรวจ)

INSERT INTO students VALUES
    ('STU006', 'นภา ฟ้าใส', 4, 'ก', 3.40, '2551-06-01');

UPDATE students SET section = 'ค' WHERE student_id = 'STU004';

SELECT student_id, full_name, gpa
FROM students
ORDER BY gpa DESC;

ALTER TABLE students ADD COLUMN nickname TEXT;
UPDATE students SET nickname = 'ชาย' WHERE student_id = 'STU001';

SELECT section, COUNT(*) AS จำนวน
FROM students
GROUP BY section;
