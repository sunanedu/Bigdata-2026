-- Lab 2.3 — เฉลย

SELECT s.full_name, e.subj_id, e.score
FROM students s
INNER JOIN enrollments e ON s.student_id = e.std_id;

SELECT s.student_id, s.full_name, e.score
FROM students s
LEFT JOIN enrollments e ON s.student_id = e.std_id
ORDER BY s.student_id;

SELECT sub.subj_name, ROUND(AVG(e.score), 2) AS คะแนนเฉลี่ย
FROM subjects sub
INNER JOIN enrollments e ON sub.subj_id = e.subj_id
GROUP BY sub.subj_id, sub.subj_name;

SELECT s.full_name, e.score
FROM students s
INNER JOIN enrollments e ON s.student_id = e.std_id
INNER JOIN subjects sub ON e.subj_id = sub.subj_id
WHERE sub.subj_name = 'คณิตศาสตร์' AND e.score >= 80;

SELECT s.full_name, e.score
FROM students s
INNER JOIN enrollments e ON s.student_id = e.std_id
WHERE e.score > (SELECT AVG(score) FROM enrollments);
