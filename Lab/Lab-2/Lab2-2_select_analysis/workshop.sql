-- Workshop 2.2 — วิเคราะห์อุบัติเหตุทางถนน (บทที่ 2.2)
-- ฐานข้อมูล: output/road_accidents.db | ตาราง road_accidents

-- โจทย์ 1: Top 5 สาเหตุที่เกิดบ่อยที่สุด
SELECT สาเหตุหลักของอุบัติเหตุ, COUNT(*) AS จำนวน
FROM road_accidents
GROUP BY สาเหตุหลักของอุบัติเหตุ
ORDER BY จำนวน DESC
LIMIT 5;

-- โจทย์ 2: อุบัติเหตุในช่วงกลางคืน เสียชีวิตสูงสุด (Top 10 จังหวัด)
SELECT จังหวัด, COUNT(*) AS จำนวน, SUM(จำนวนผู้เสียชีวิต) AS เสียชีวิต
FROM road_accidents
WHERE ช่วงเวลากลางวัน_กลางคืน = 'กลางคืน'
GROUP BY จังหวัด
HAVING SUM(จำนวนผู้เสียชีวิต) > 0
ORDER BY เสียชีวิต DESC
LIMIT 10;

-- โจทย์ 3: เปรียบเทียบวันหยุด vs วันปกติ
SELECT
    วันหยุด_วันปกติ,
    COUNT(*) AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต) AS รวมเสียชีวิต,
    ROUND(AVG(ค่าใช้จ่ายรวม_บาท), 0) AS คชจ_เฉลี่ย
FROM road_accidents
GROUP BY วันหยุด_วันปกติ;
