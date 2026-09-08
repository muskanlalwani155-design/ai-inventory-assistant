import os
import sys
import streamlit as st
import pandas as pd

# Path fix
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import execute_query
from ai_service import generate_sql, is_safe_query, client

st.set_page_config(
    page_title="AI Inventory Assistant",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 AI-Powered Inventory & Analytics Dashboard")
st.caption("Ask questions in plain English to query live MySQL inventory data.")

# Sidebar: Live DB Explorer
with st.sidebar:
    st.header("🗄️ Database Explorer")
    table_choice = st.selectbox(
        "Select Table to Inspect:",
        ["products", "categories", "orders", "order_items"]
    )
    if st.button("Fetch Table Records", use_container_width=True):
        records = execute_query(f"SELECT * FROM {table_choice} LIMIT 20;")
        if records:
            st.dataframe(pd.DataFrame(records), use_container_width=True)
        else:
            st.info("Table is empty or no records found.")

# Session chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purane messages render karna
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "sql" in msg and msg["sql"]:
            st.code(msg["sql"], language="sql")
        if "data" in msg and msg["data"]:
            st.dataframe(pd.DataFrame(msg["data"]), use_container_width=True)

# User Chat Input
if prompt := st.chat_input("Ask a question (e.g., 'Show the top 3 most expensive products')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        sql_query = None
        results = None
        summary_text = ""

        try:
            with st.spinner("1/3 Generating SQL..."):
                sql_query = generate_sql(prompt)

            st.markdown("**Generated SQL:**")
            st.code(sql_query, language="sql")

            # Security check
            if not is_safe_query(sql_query):
                err_text = "⚠️ Query Blocked: Only read-only SELECT queries are allowed."
                st.error(err_text)
                st.session_state.messages.append({"role": "assistant", "content": err_text, "sql": sql_query})
            else:
                with st.spinner("2/3 Executing on MySQL..."):
                    results = execute_query(sql_query)

                if results is None:
                    err_text = "❌ Database execution failed. Check query syntax or DB connection."
                    st.error(err_text)
                    st.session_state.messages.append({"role": "assistant", "content": err_text, "sql": sql_query})
                elif len(results) == 0:
                    info_text = "Database returned 0 matching records."
                    st.info(info_text)
                    st.session_state.messages.append({"role": "assistant", "content": info_text, "sql": sql_query})
                else:
                    # Pehle table render kar do taaki UI freeze na lage
                    st.markdown("**Query Results:**")
                    st.dataframe(pd.DataFrame(results), use_container_width=True)

                    # Summary generation with fallback
                    try:
                        with st.spinner("3/3 Summarizing insights..."):
                            summary_prompt = f"""
                            User Question: {prompt}
                            SQL Query: {sql_query}
                            Database Results: {results}

                            Provide a concise, direct 1-2 sentence business response answering the question using this data.
                            """
                            summary_res = client.models.generate_content(
                                model="gemini-2.5-flash-lite",
                                contents=summary_prompt
                            )
                            summary_text = summary_res.text.strip()
                            st.markdown(summary_text)
                    except Exception as ai_err:
                        summary_text = "Data fetched successfully from database (Summary skipped due to API timeout)."
                        st.caption(summary_text)

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": summary_text,
                        "sql": sql_query,
                        "data": results
                    })

        except Exception as e:
            st.error(f"Error occurred: {e}")