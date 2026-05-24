INSERT INTO students VALUES
    ('STU001', 'สมใจ ใจดี', 4, 'parent_daeng'),
    ('STU002', 'มานี มีสุข', 4, 'parent_daeng'),
    ('STU003', 'วิชัย ขยัน', 5, NULL);

INSERT INTO teachers VALUES
    ('T001', 'ครูวิชัย สอนดี', 45000, '081-100-0001'),
    ('T002', 'ครูสมหญิง ใจเย็น', 48000, '081-100-0002');

INSERT INTO subjects VALUES
    ('MAT101', 'คณิตศาสตร์', 3),
    ('ENG101', 'ภาษาอังกฤษ', 3),
    ('SCI101', 'วิทยาศาสตร์', 3);

INSERT INTO grades VALUES
    ('G001', 'STU001', 'MAT101', 85, '2568/1'),
    ('G002', 'STU001', 'ENG101', 72, '2568/1'),
    ('G003', 'STU002', 'MAT101', 91, '2568/1'),
    ('G004', 'STU003', 'SCI101', 68, '2568/1');

INSERT INTO schedule VALUES
    ('SCH01', 'MAT101', 'จันทร์', 1),
    ('SCH02', 'ENG101', 'อังคาร', 2),
    ('SCH03', 'SCI101', 'พุธ', 3);

-- password จะถูก hash โดย setup_lab.py (placeholder)
INSERT INTO users (username, password_hash, salt, role) VALUES
    ('admin_it', 'pending', 'pending', 'admin'),
    ('teacher_wichai', 'pending', 'pending', 'teacher'),
    ('student_somjai', 'pending', 'pending', 'student'),
    ('parent_daeng', 'pending', 'pending', 'parent');
