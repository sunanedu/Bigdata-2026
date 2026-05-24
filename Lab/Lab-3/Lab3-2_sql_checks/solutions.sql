-- Lab 3.2 — เฉลย (ตาราง dirty_records หลัง import CSV)

SELECT COUNT(*) FROM dirty_records;

SELECT
    SUM(CASE WHEN จังหวัด IS NULL THEN 1 ELSE 0 END) AS null_จังหวัด,
    SUM(CASE WHEN ความรุนแรง IS NULL THEN 1 ELSE 0 END) AS null_ความรุนแรง,
    SUM(CASE WHEN อายุ_ปี IS NULL THEN 1 ELSE 0 END) AS null_อายุ
FROM dirty_records;

SELECT accident_id, COUNT(*) AS n
FROM dirty_records
GROUP BY accident_id
HAVING COUNT(*) > 1;

SELECT accident_id, จำนวนผู้เสียชีวิต, ความรุนแรง
FROM dirty_records
WHERE CAST(จำนวนผู้เสียชีวิต AS INTEGER) > 0
  AND ความรุนแรง = 'ไม่บาดเจ็บ';

SELECT
    SUM(CASE
        WHEN จังหวัด IS NOT NULL
         AND ความรุนแรง IS NOT NULL
         AND อายุ_ปี IS NOT NULL
         AND CAST(อายุ_ปี AS REAL) BETWEEN 5 AND 100
         AND CAST(เดือน AS INTEGER) BETWEEN 1 AND 12
        THEN 1 ELSE 0
    END) AS ผ่านเกณฑ์,
    SUM(CASE
        WHEN NOT (
            จังหวัด IS NOT NULL
            AND ความรุนแรง IS NOT NULL
            AND อายุ_ปี IS NOT NULL
            AND CAST(อายุ_ปี AS REAL) BETWEEN 5 AND 100
            AND CAST(เดือน AS INTEGER) BETWEEN 1 AND 12
        ) THEN 1 ELSE 0
    END) AS ไม่ผ่านเกณฑ์
FROM dirty_records;
