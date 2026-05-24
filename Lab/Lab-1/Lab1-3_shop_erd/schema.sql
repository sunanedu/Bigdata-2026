-- Lab 1.3: ร้านป้าแดง — สร้างตารางตาม ERD (เอกสารหน่วยที่ 1)

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    cust_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    cust_name TEXT    NOT NULL,
    phone     TEXT,
    address   TEXT
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_name  TEXT    NOT NULL,
    price      REAL    NOT NULL,
    category   TEXT,
    stock_qty  INTEGER DEFAULT 0
);

CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    cust_id     INTEGER NOT NULL REFERENCES customers(cust_id),
    order_date  DATE    NOT NULL,
    total_price REAL
);

CREATE TABLE order_items (
    item_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id   INTEGER NOT NULL REFERENCES orders(order_id),
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    quantity   INTEGER NOT NULL,
    unit_price REAL    NOT NULL
);
