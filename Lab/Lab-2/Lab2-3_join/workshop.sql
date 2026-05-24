-- Workshop 2.3 — JOIN 3 ตาราง (บทที่ 2.3)
-- ฐานข้อมูล: output/school_join.db

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
