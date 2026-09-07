import sys
from db import execute_query
from ai_service import generate_sql, is_safe_query, client

def summarize_data(user_question: str, query: str, data: list) -> str:
    if not data:
        return "No records related to this question were found in the database."

    prompt = f"""
    You are an intelligent business assistant.
    User Question: {user_question}
    Executed SQL Query: {query}
    Database Result: {data}
    
    Instructions:
    Provide a concise, professional answer directly addressing the user's question using the database results.
    Keep the tone polite and clear.
"""
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    return response.text.strip()

def run_assistant():
    print("="*60)
    print("         AI-POWERED INVENTORY & BUSINESS ANALYTICS ASSISTANT         ")
    print("="*60)
    print("Type 'Exit' or 'Quit' to close the program.\n")

    while True:
        try: 
            user_question = input("\nYour Question:" ).strip()

            if not user_question:
                continue

            if user_question.lower() in ["exit", "quit"]:
                print("\nThe assistant is shutting down. Goodbye!")
                break

            print("\n[1/3]  Generating the SQL query using AI...")
            sql_query = generate_sql(user_question)
            print(f"Generated SQL: {sql_query}")

            print("\n [2/3] Verifying the query security...")
            if not is_safe_query(sql_query):
                print("Error: A destructive or unsafe query was detected. Action blocked")
                continue

            print("\n [3/3] Fetching data from the MySQL database..")
            results = execute_query(sql_query)

            if results is None:
                print("Database execution error. Please check whether the query was correct.")
                continue

            print("\n" + "-" * 40)
            final_summary = summarize_data(user_question, sql_query, results)
            print(f"Assistant: {final_summary}")
            print("-" * 40)

        except KeyboardInterrupt:
            print("\nProgram closed.")
            sys.exit(0)
        except Exception as err:
            print(f"Unexpected Error: {err}")    

if __name__ == "__main__":
    run_assistant()









    