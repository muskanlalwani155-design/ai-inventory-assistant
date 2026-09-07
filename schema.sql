CREATE DATABASE IF NOT EXISTS inventory_db;
USE inventory_db;

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;


CREATE TABLE categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category_id INT,
    price DECIMAL(10, 2) NOT NULL, 
    stock_quantity INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00

);

CREATE TABLE order_items (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE RESTRICT
);


-- sample mock data for testing 

INSERT INTO categories 
(category_name)
VALUES 
("Electronics"),
("Accessories"),
("Stationery");

INSERT INTO products 
(product_name, category_id, price, stock_quantity)
VALUES
("Wireless Mouse", 1, 799.00, 25),
("Mechanical Keyboard", 1, 2499.00, 10),
("USB-C Hub", 2, 1299.00, 5),
("Laptop Stand", 2, 890.00, 15),
("Notebook Spiral", 3, 150.00, 50);









