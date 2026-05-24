-- Lab 2.4 — TRANSACTION ตัวอย่าง
-- ฐานข้อมูล: output/bank_demo.db (สร้างโดย setup_lab.py)

-- โอนเงิน 5,000 จาก ACC001 → ACC002
BEGIN;

UPDATE bank_accounts
SET balance = balance - 5000
WHERE account_id = 'ACC001';

UPDATE bank_accounts
SET balance = balance + 5000
WHERE account_id = 'ACC002';

COMMIT;

SELECT account_id, balance FROM bank_accounts;

-- ทดลอง ROLLBACK (รันทีละบล็อก — อย่า COMMIT)
-- BEGIN;
-- UPDATE bank_accounts SET balance = balance - 99999 WHERE account_id = 'ACC001';
-- ROLLBACK;
