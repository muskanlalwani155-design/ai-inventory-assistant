import os
import re
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# giving inforamtion of our database to ai 
DB_SCHEMA = """
Database: inventory_db
Tables:
1. categories (category_id INT PK, category_name VARCHAR)
2. products (product_id INT PK, product_name VARCHAR, category_id INT FK, price DECIMAL, stock_quantity INT, created_at TIMESTAMP)
3. orders (order_id INT PK, customer_name VARCHAR, order_date TIMESTAMP, total_amount DECIMAL)
4. order_items (order_item_id INT PK, order_id INT FK, product_id INT FK, quantity INT, unit_price DECIMAL)
"""


# convert question to sql query
def generate_sql(user_question: str) -> str:

    prompt = f"""
        You are an expert MySQL developer. Given the database schema below, 
        translate the user's natural language question into a valid MySQL SELECT query.
        Schema:
        {DB_SCHEMA}

        Rules: 
        1. Return ONLY the raw SQL query. Do NOT add markdown blocks, 
        no ```sql, and no explanation.
        2. Only write SELECT queries. Never generate INSERT, UPDATE, DELETE, DROP, or ALTER.
        3. Use proper JOINs where table relationships are required.

        User Question : {user_question}
        SQL Query:

        """
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    sql_query = response.text.strip().replace("```sql", "").replace("```", "").strip()
    return sql_query

def is_safe_query(query: str) -> bool:
    forbidden_keywords = [
        r"\bDROP\b", 
        r"\bDELETE\b", 
        r"\bUPDATE\b", 
        r"\bINSERT\b", 
        r"\bALTER\b", 
        r"\bTRUNCATE\b"]
    for keyword in forbidden_keywords:
        if re.search(keyword, query, re.IGNORECASE):
            return False
    return query.strip().upper().startswith("SELECT")



if __name__ == "__main__":
    test_question = "Which products have price greater than 1000?"
    generated_sql = generate_sql(test_question)
    print("Generated SQL:", generated_sql)
    print("Is Query Safe?", is_safe_query(generated_sql))