import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        host = os.getenv("DB_HOST", "localhost")
        config = {
            "host": host,
            "port": int(os.getenv("DB_PORT", 3307)),
            "user": os.getenv("DB_USER", "root"),
            "password": os.getenv("DB_PASSWORD", "root123"),
            "database": os.getenv("DB_NAME", "inventory_db"),
        }

        
        if host != "localhost":
            ca_path = "/etc/ssl/certs/ca-certificates.crt"
            if os.path.exists(ca_path):
                config["ssl_ca"] = ca_path
            config["ssl_verify_cert"] = True

        return mysql.connector.connect(**config)
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
