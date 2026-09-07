import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3307)),
            user=os.getenv("DB_USER", "root"),  
            password=os.getenv("DB_PASSWORD", "root123"),
            database=os.getenv("DB_NAME", "inventory_db")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

def execute_query(query, params=None):
    conn = get_db_connection()
    if not conn:
        return None   

    try: 
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Query Execution Error: {err}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()    

if __name__ == "__main__":
    data = execute_query('SELECT * FROM products;')
    print("Database Result:", data)