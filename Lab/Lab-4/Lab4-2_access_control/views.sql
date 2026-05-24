-- VIEW สำหรับ Row-Level Security (MySQL / SQLite)
-- รันหลัง seed ข้อมูล

DROP VIEW IF EXISTS v_grades_somjai;
CREATE VIEW v_grades_somjai AS
SELECT g.grade_id, g.student_id, s.subject_name, g.score, g.semester
FROM grades g
JOIN subjects s ON g.subject_id = s.subject_id
WHERE g.student_id = 'STU001';

DROP VIEW IF EXISTS v_grades_child_daeng;
CREATE VIEW v_grades_child_daeng AS
SELECT g.grade_id, st.full_name AS student_name, s.subject_name, g.score
FROM grades g
JOIN students st ON g.student_id = st.student_id
JOIN subjects s ON g.subject_id = s.subject_id
WHERE st.parent_username = 'parent_daeng';
