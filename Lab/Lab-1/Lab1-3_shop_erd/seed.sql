-- ข้อมูลตัวอย่างร้านป้าแดง

INSERT INTO customers (cust_name, phone, address) VALUES
    ('คุณแดง', '081-111-1111', 'ซ.สุขุม 1'),
    ('ลุงสมบัติ', '082-222-2222', 'หมู่บ้านสวนดอก'),
    ('ป้าจิต', '083-333-3333', 'ตลาดเช้า');

INSERT INTO products (prod_name, price, category, stock_qty) VALUES
    ('น้ำดื่ม 600ml', 7, 'เครื่องดื่ม', 120),
    ('ขนมปังโฮลวีท', 25, 'อาหาร', 45),
    ('ไข่ไก่ 10 ฟอง', 45, 'อาหาร', 80),
    ('นม UHT 1 ลิตร', 38, 'เครื่องดื่ม', 60),
    ('สบู่ก้อน', 15, 'ของใช้', 200);

INSERT INTO orders (cust_id, order_date, total_price) VALUES
    (1, '2568-01-15', 32),
    (2, '2568-01-16', 70),
    (1, '2568-01-20', 53);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 2, 7),
    (1, 2, 1, 25),
    (2, 3, 1, 45),
    (2, 4, 1, 38),
    (3, 4, 1, 38),
    (3, 5, 1, 15);
