import ssl
import mysql.connector

print("1. Connecting to TiDB Cloud...")

# TiDB Cloud requires SSL; using system default context with pure python engine
ssl_ctx = ssl.create_default_context()

db_config = {
    "host": "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "3UKqkEc7DXYGh4q.root",
    "password": "Vkxmytl7vErny2ye",
    "use_pure": True,
    "ssl_ca": None,
    "ssl_disabled": False,
}

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("2. Connection successful!")

    # Database create
    cursor.execute("CREATE DATABASE IF NOT EXISTS inventory_db;")
    cursor.execute("USE inventory_db;")
    print("3. Database 'inventory_db' ready.")

    # Tables create
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS categories (
        category_id INT AUTO_INCREMENT PRIMARY KEY,
        category_name VARCHAR(100) NOT NULL
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(150) NOT NULL,
        category_id INT,
        price DECIMAL(10, 2) NOT NULL,
        stock_quantity INT NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
    );
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        quantity INT NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """
    )
    print("4. Tables created successfully.")

    # Check and insert initial data
    cursor.execute("SELECT COUNT(*) FROM products;")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            """
        INSERT INTO categories (category_name) VALUES 
        ('Electronics'), ('Accessories'), ('Office Supplies');
        """
        )
        cursor.execute(
            """
        INSERT INTO products (product_name, category_id, price, stock_quantity) VALUES 
        ('Wireless Mouse', 2, 499.00, 50),
        ('Mechanical Keyboard', 2, 2499.00, 30),
        ('24-inch Monitor', 1, 8999.00, 15),
        ('USB-C Hub', 2, 1299.00, 25),
        ('Ergonomic Chair', 3, 7500.00, 10);
        """
        )
        conn.commit()
        print("5. Initial sample data inserted.")
    else:
        print(f"5. Products already exist ({count} rows).")

    cursor.close()
    conn.close()
    print("--> SUCCESS: Cloud Database is 100% Ready!")

except Exception as e:
    print("ERROR:", e)