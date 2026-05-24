-- Lab 3.2 — แบบฝึก SQL (ทำบน output/road_accidents.db และ data/dirty_records ใน SQLite)

-- โจทย์ A: สร้างตาราง dirty ใน DB Browser
--   File → Import → dirty_records.csv → ชื่อตาราง dirty_records
--   แล้วทำข้อ 1–5 บนตาราง dirty_records

-- 1) นับแถวทั้งหมดใน dirty_records


-- 2) นับ NULL ใน จังหวัด, ความรุนแรง, อายุ_ปี (ใช้ CASE WHEN)


-- 3) หา accident_id ที่ซ้ำ


-- 4) หาความขัดแย้ง: จำนวนผู้เสียชีวิต > 0 แต่ความรุนแรง = 'ไม่บาดเจ็บ'


-- 5) เปรียบเทียบ: จำนวนแถวที่ผ่านเกณฑ์ vs ไม่ผ่าน (ใช้ CASE สรุป 2 กลุ่ม)
