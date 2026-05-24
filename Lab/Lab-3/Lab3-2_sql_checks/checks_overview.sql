-- Lab 3.2 — กระบวนการตรวจสอบ 6 ขั้น (บทที่ 3.2)

-- ขั้น 1: สำรวจเบื้องต้น
SELECT COUNT(*) FROM road_accidents;
SELECT accident_id, วันที่เกิดเหตุ, จังหวัด, ความรุนแรง, อายุ_ปี
FROM road_accidents LIMIT 5;

-- ขั้น 2: NULL (เปอร์เซ็นต์)
SELECT
    'อายุ_ปี' AS คอลัมน์,
    SUM(CASE WHEN อายุ_ปี IS NULL THEN 1 ELSE 0 END) AS จำนวน_NULL,
    ROUND(SUM(CASE WHEN อายุ_ปี IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_NULL
FROM road_accidents;

-- ขั้น 3: ซ้ำ
SELECT accident_id, COUNT(*) AS n
FROM road_accidents GROUP BY accident_id HAVING COUNT(*) > 1;

-- ขั้น 4: ช่วงค่า
SELECT MIN(อายุ_ปี), MAX(อายุ_ปี), MAX(ความเร็วโดยประมาณ_กมชม) FROM road_accidents;

-- ขั้น 5: ความสอดคล้อง
SELECT accident_id, จำนวนผู้เสียชีวิต, ความรุนแรง
FROM road_accidents
WHERE จำนวนผู้เสียชีวิต > 0 AND ความรุนแรง = 'ไม่บาดเจ็บ';

-- ขั้น 6: จังหวัดที่มีช่องว่างแฝง
SELECT จังหวัด, LENGTH(จังหวัด) AS len
FROM road_accidents
WHERE จังหวัด != TRIM(จังหวัด)
LIMIT 10;
