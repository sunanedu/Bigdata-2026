-- ตรวจสอบหลัง Workshop 5.2
-- เปิด output/school_data.db

SELECT COUNT(*) AS จำนวน FROM accidents_api;

SELECT accident_id, วันที่, จังหวัด, ผู้เสียชีวิต, ผู้บาดเจ็บ
FROM accidents_api
WHERE ผู้เสียชีวิต > 0
ORDER BY ผู้เสียชีวิต DESC
LIMIT 10;

SELECT จังหวัด, COUNT(*) AS จำนวน
FROM accidents_api
GROUP BY จังหวัด
ORDER BY จำนวน DESC
LIMIT 5;
