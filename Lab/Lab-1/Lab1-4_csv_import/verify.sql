-- Lab 1.4: ตรวจสอบหลังนำเข้า CSV (บทที่ 1.4)

-- 1) นับจำนวนแถวทั้งหมด (ชุดเต็ม ~20,000 | ตัวอย่างใน repo ~5,000)
SELECT COUNT(*) AS จำนวนแถวทั้งหมด FROM road_accidents;

-- 2) ดูตัวอย่าง 5 แถวแรก
SELECT accident_id, วันที่เกิดเหตุ, จังหวัด, ความรุนแรง
FROM road_accidents
LIMIT 5;

-- 3) ดูชื่อคอลัมน์ทั้งหมด
PRAGMA table_info(road_accidents);

-- 4) สถิติภาพรวม (ผลโดยประมาณจากเอกสาร)
SELECT
    COUNT(*) AS จำนวนอุบัติเหตุ_ครั้ง,
    SUM(จำนวนผู้เสียชีวิต) AS ผู้เสียชีวิต_ราย,
    SUM(จำนวนผู้บาดเจ็บ) AS ผู้บาดเจ็บ_ราย
FROM road_accidents;

-- 5) ยานพาหนะที่เกิดเหตุมากที่สุด
SELECT ประเภทยานพาหนะหลัก, COUNT(*) AS จำนวน
FROM road_accidents
GROUP BY ประเภทยานพาหนะหลัก
ORDER BY จำนวน DESC
LIMIT 5;
