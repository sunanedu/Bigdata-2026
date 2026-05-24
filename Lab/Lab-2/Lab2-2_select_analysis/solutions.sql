-- Lab 2.2 — เฉลย

SELECT
    COUNT(*) AS จำนวนอุบัติเหตุ,
    SUM(จำนวนผู้เสียชีวิต) AS รวมเสียชีวิต,
    SUM(จำนวนผู้บาดเจ็บ) AS รวมบาดเจ็บ,
    ROUND(AVG(ค่าใช้จ่ายรวม_บาท), 0) AS คชจ_เฉลี่ย,
    MAX(ค่าใช้จ่ายรวม_บาท) AS คชจ_สูงสุด
FROM road_accidents;

SELECT จังหวัด, COUNT(*) AS จำนวนเหตุ
FROM road_accidents
GROUP BY จังหวัด
ORDER BY จำนวนเหตุ DESC
LIMIT 5;

SELECT accident_id, จังหวัด, ความรุนแรง, จำนวนผู้เสียชีวิต
FROM road_accidents
WHERE จังหวัด = 'เชียงใหม่'
  AND ความรุนแรง IN ('เสียชีวิต', 'บาดเจ็บสาหัส');

SELECT DISTINCT จังหวัด
FROM road_accidents
WHERE จังหวัด LIKE 'นคร%';

SELECT
    สาเหตุหลักของอุบัติเหตุ,
    COUNT(*) AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต) AS รวมเสียชีวิต
FROM road_accidents
GROUP BY สาเหตุหลักของอุบัติเหตุ
HAVING SUM(จำนวนผู้เสียชีวิต) > 30
ORDER BY รวมเสียชีวิต DESC;

SELECT เดือน, COUNT(*) AS จำนวนเหตุ
FROM road_accidents
WHERE เดือน BETWEEN 1 AND 3
GROUP BY เดือน
ORDER BY เดือน;

SELECT accident_id, จังหวัด, ค่าใช้จ่ายรวม_บาท
FROM road_accidents
ORDER BY ค่าใช้จ่ายรวม_บาท DESC
LIMIT 5;
