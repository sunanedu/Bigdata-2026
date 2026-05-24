-- Workshop 3.2 — ตรวจสอบคุณภาพข้อมูล 10 ข้อ
-- ฐานข้อมูล: output/road_accidents.db

-- 1) นับจำนวน Record ทั้งหมด
SELECT COUNT(*) AS จำนวน_records_ทั้งหมด
FROM road_accidents;

-- 2) หา NULL ในคอลัมน์ อายุ_ปี
SELECT COUNT(*) AS แถวที่อายุ_NULL
FROM road_accidents
WHERE อายุ_ปี IS NULL;

SELECT accident_id, วันที่เกิดเหตุ, จังหวัด, อายุ_ปี
FROM road_accidents
WHERE อายุ_ปี IS NULL
LIMIT 10;

-- 3) หา NULL ในคอลัมน์ จังหวัด
SELECT COUNT(*) AS แถวที่จังหวัด_NULL
FROM road_accidents
WHERE จังหวัด IS NULL;

-- 4) ตรวจ accident_id ซ้ำ
SELECT
    COUNT(*) AS จำนวนทั้งหมด,
    COUNT(DISTINCT accident_id) AS จำนวน_unique,
    COUNT(*) - COUNT(DISTINCT accident_id) AS จำนวนที่ซ้ำ
FROM road_accidents;

SELECT accident_id, COUNT(*) AS จำนวนครั้ง
FROM road_accidents
GROUP BY accident_id
HAVING COUNT(*) > 1;

-- 5) หาอายุที่เป็นไปไม่ได้ (< 0 หรือ > 100)
SELECT accident_id, อายุ_ปี, วันที่เกิดเหตุ
FROM road_accidents
WHERE อายุ_ปี < 0 OR อายุ_ปี > 100;

-- 6) หาความเร็วที่สูงผิดปกติ (> 200)
SELECT accident_id, ความเร็วโดยประมาณ_กมชม, ประเภทยานพาหนะหลัก
FROM road_accidents
WHERE ความเร็วโดยประมาณ_กมชม > 200;

-- 7) หาเดือนที่ผิด (< 1 หรือ > 12)
SELECT accident_id, เดือน, วันที่เกิดเหตุ
FROM road_accidents
WHERE เดือน < 1 OR เดือน > 12;

-- 8) หาความรุนแรงที่ไม่อยู่ในรายการ
SELECT DISTINCT ความรุนแรง
FROM road_accidents
WHERE ความรุนแรง NOT IN (
    'เสียชีวิต', 'บาดเจ็บสาหัส',
    'บาดเจ็บปานกลาง', 'บาดเจ็บเล็กน้อย', 'ไม่บาดเจ็บ'
);

-- 9) ตรวจความขัดแย้งเรื่องความเร็ว (บอกว่าเกิน แต่ความเร็ว <= จำกัด)
SELECT accident_id,
       ความเร็วโดยประมาณ_กมชม,
       จำกัดความเร็ว_กมชม,
       เกินความเร็ว_ใช่ไม่ใช่
FROM road_accidents
WHERE เกินความเร็ว_ใช่ไม่ใช่ = 'ใช่'
  AND ความเร็วโดยประมาณ_กมชม <= จำกัดความเร็ว_กมชม;

-- 10) นับ Record ที่ผ่านเกณฑ์พื้นฐาน (ตัวอย่างเกณฑ์)
SELECT COUNT(*) AS แถวที่ผ่านเกณฑ์
FROM road_accidents
WHERE accident_id IS NOT NULL
  AND จังหวัด IS NOT NULL
  AND อายุ_ปี BETWEEN 0 AND 100
  AND เดือน BETWEEN 1 AND 12
  AND ความเร็วโดยประมาณ_กมชม <= 200
  AND ความรุนแรง IN (
      'เสียชีวิต', 'บาดเจ็บสาหัส',
      'บาดเจ็บปานกลาง', 'บาดเจ็บเล็กน้อย', 'ไม่บาดเจ็บ'
  );
