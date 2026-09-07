import mysql.connector
from db import get_db_connection

def place_order(customer_name: str, items: list) -> dict:
    """
    ACID Compliant Order Placement:
    items format: [
    {'product_id': 1, 'quantity': 2}, 
    {'product_id': 3, 'quantity': 1}
    ]
    """

    conn = get_db_connection()
    if not conn:
        return {"status": "error", "message": "Database connection failed"}

    try:
        conn.autocommit = False
        cursor = conn.cursor(dictionary=True)

        total_amount = 0.0
        verified_items = []

        for item in items:
            product_id = item["product_id"]
            requested_qty = item["quantity"]

            cursor.execute(
                "SELECT product_id, product_name, price, stock_quantity FROM products WHERE product_id = %s FOR UPDATE;",
                (product_id,)
            )
            product = cursor.fetchone()

            if not product:
                conn.rollback()
                return {"status": "error", "message": f"Product ID {product_id} does not exist."}

            if product["stock_quantity"] < requested_qty:
                conn.rollback()
                return {
                    "status": "error",
                    "message": f"Insufficient stock for '{product['product_name']}'. Available: {product['stock_quantity']}, Requested: {requested_qty}"
                }

            item_total = float(product["price"]) * requested_qty
            total_amount += item_total
            verified_items.append({
                "product_id": product_id,
                "quantity": requested_qty,
                "unit_price": product["price"]
            })

            cursor.execute(
                "INSERT INTO orders (customer_name, total_amount) VALUES (%s, %s)",
                (customer_name, total_amount)
            )
            order_id = cursor.lastrowid

            for item in verified_items:
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s);",
                    (order_id, item["product_id"], item["quantity"], item["unit_price"])
                )
                cursor.execute(
                "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s;",
                (item["quantity"], item["product_id"])
            )
        conn.commit()
        return {
            "status": "success",
            "message": "Order successfully placed!",
            "order_id": order_id,
            "total_amount": total_amount
        }    
    except mysql.connector.Error as err:
        conn.rollback()
        return {"status": "error", "message": f"Transaction failed: {err}"}

    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close() 


if __name__ == "__main__":
    # Test 1: Successful Order
    print("--- Test 1: Valid Order ---")
    result = place_order("Muskan Lalwani", [{"product_id": 1, "quantity": 2}])
    print(result)

    # Test 2: Over-stock Order (Rollback test)
    print("\n--- Test 2: Invalid Order (Stock check) ---")
    result_fail = place_order("Test User", [{"product_id": 3, "quantity": 999}])
    print(result_fail)            








