-- Workshop 4.2 — GRANT / REVOKE ระบบโรงเรียน (MySQL)
-- รันบน MySQL Server หลังสร้างฐานข้อมูล school_db จาก schema ในโฟลเดอร์นี้

-- สร้าง User 4 คน
CREATE USER IF NOT EXISTS 'admin_it'@'localhost' IDENTIFIED BY 'Adm1n#Sup3r!';
CREATE USER IF NOT EXISTS 'teacher_wichai'@'localhost' IDENTIFIED BY 'T3ach3r#2026';
CREATE USER IF NOT EXISTS 'student_somjai'@'localhost' IDENTIFIED BY 'St4d3nt#2026';
CREATE USER IF NOT EXISTS 'parent_daeng'@'localhost' IDENTIFIED BY 'P4r3nt#2026';

-- ผู้ดูแลระบบ
GRANT ALL PRIVILEGES ON school_db.* TO 'admin_it'@'localhost';

-- ครู: อ่าน/บันทึกเกรด, ดูนักเรียน
GRANT SELECT, INSERT, UPDATE ON school_db.grades TO 'teacher_wichai'@'localhost';
GRANT SELECT ON school_db.students TO 'teacher_wichai'@'localhost';
GRANT SELECT ON school_db.subjects TO 'teacher_wichai'@'localhost';
GRANT SELECT, UPDATE ON school_db.schedule TO 'teacher_wichai'@'localhost';
GRANT SELECT ON school_db.teachers TO 'teacher_wichai'@'localhost';

-- นักเรียน: ดูวิชา/ตารางเรียน, เกรดผ่าน VIEW เท่านั้น
GRANT SELECT ON school_db.subjects TO 'student_somjai'@'localhost';
GRANT SELECT ON school_db.schedule TO 'student_somjai'@'localhost';
GRANT SELECT ON school_db.v_grades_somjai TO 'student_somjai'@'localhost';

-- ผู้ปกครอง: ดูเกรดบุตรผ่าน VIEW
GRANT SELECT ON school_db.subjects TO 'parent_daeng'@'localhost';
GRANT SELECT ON school_db.v_grades_child_daeng TO 'parent_daeng'@'localhost';

FLUSH PRIVILEGES;

-- ข้อ 4: ถอนสิทธิ์ student จาก teachers (ถ้าเคยให้ไว้)
REVOKE ALL PRIVILEGES ON school_db.teachers FROM 'student_somjai'@'localhost';
FLUSH PRIVILEGES;

-- ตรวจสอบสิทธิ์
SHOW GRANTS FOR 'teacher_wichai'@'localhost';
SHOW GRANTS FOR 'student_somjai'@'localhost';
