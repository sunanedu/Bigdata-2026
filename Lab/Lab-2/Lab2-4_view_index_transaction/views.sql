-- Lab 2.4 — VIEW, INDEX (บทที่ 2.4)
-- ฐานข้อมูล: output/road_accidents.db

DROP VIEW IF EXISTS v_province_summary;

CREATE VIEW v_province_summary AS
SELECT
    จังหวัด,
    ภูมิภาค,
    COUNT(*)                         AS จำนวนเหตุ,
    SUM(จำนวนผู้เสียชีวิต)            AS รวมเสียชีวิต,
    SUM(จำนวนผู้บาดเจ็บ)             AS รวมบาดเจ็บ,
    ROUND(AVG(ค่าใช้จ่ายรวม_บาท), 0) AS คชจ_เฉลี่ย,
    SUM(ค่าใช้จ่ายรวม_บาท)           AS คชจ_รวม
FROM road_accidents
GROUP BY จังหวัด, ภูมิภาค;

-- ทดสอบ VIEW
SELECT * FROM v_province_summary
WHERE ภูมิภาค = 'ภาคเหนือ'
ORDER BY จำนวนเหตุ DESC
LIMIT 10;

-- INDEX
CREATE INDEX IF NOT EXISTS idx_province ON road_accidents(จังหวัด);
CREATE INDEX IF NOT EXISTS idx_province_date ON road_accidents(จังหวัด, วันที่เกิดเหตุ);

PRAGMA index_list(road_accidents);
