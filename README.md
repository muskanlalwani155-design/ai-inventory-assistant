# AI-Powered Inventory & Analytics Assistant

An intelligent full-stack conversational analytics dashboard that translates natural language business questions into executable SQL queries, fetches real-time data from a cloud MySQL database, and synthesizes direct operational insights using Google Gemini AI[cite: 7].

---

**Live Application:** [View Live Streamlit Demo](https://muskanlalwani155-design-ai-inventory-assistant.streamlit.app/)  
**Source Code:** [GitHub Repository](https://github.com/muskanlalwani155-design/ai-inventory-assistant)[cite: 7]

---

## Tech Stack

* **Frontend & Dashboard UI**: Streamlit[cite: 7]
* **AI & LLM Engine**: Google Gemini API (`gemini-3.5-flash-lite`, Text-to-SQL & summarization)[cite: 7]
* **Database & Cloud Storage**: TiDB Cloud (Serverless MySQL 8.0 compatible)
* **Transaction Engine**: MySQL connector with support for ACID transactions[cite: 7]
* **Data Processing**: Python 3.11+, Pandas[cite: 7]
* **Deployment Platform**: Streamlit Community Cloud

---

## Architecture Overview

* **User Query (Streamlit UI)**: Captures conversational business inquiries in plain English.
* **Google Gemini API (Text-to-SQL)**: Converts natural language requests into schema-aware, optimized SQL queries using `gemini-3.5-flash-lite`[cite: 7].
* **Security & Validation Guardrails**: Restricts execution strictly to safe, read-only `SELECT` queries to avoid destructive operations.
* **Order Processing & Transactions**: Handles ACID-compliant state changes and order management via `order_service.py`[cite: 7].
* **TiDB / Cloud MySQL Database**: Executes verified queries against structured inventory and sales tables (`schema.sql`)[cite: 7].
* **Google Gemini API (Summarizer)**: Ingests raw database results and generates clear business summaries.

---

## Features

* **Natural Language to SQL**: Converts conversational inquiries into optimized SQL queries instantly.
* **ACID Transactions**: Reliable database execution for order processing and inventory updates[cite: 7].
* **Query Safety Guardrails**: Restricts ad-hoc execution strictly to read-only (`SELECT`) queries.
* **Automated Cloud DB Migration**: Dedicated setup scripts to bootstrap remote schemas seamlessly (`setup_cloud_db.py`)[cite: 7].
* **Dual Execution Modes**: Interactive web dashboard via Streamlit (`ui_app.py`) as well as CLI/terminal mode (`app.py`)[cite: 7].

---

## Project Structure

```text
ai-inventory-assistant/
├── src/
│   ├── __init__.py           # Package initializer
│   ├── ai_service.py         # Gemini API client (gemini-3.5-flash-lite), prompts & SQL safety
│   ├── app.py                # Terminal / CLI version of the assistant
│   ├── db.py                 # TiDB/MySQL connection handler & query executor
│   ├── order_service.py      # Inventory transactions & ACID-compliant order operations
│   ├── setup_cloud_db.py     # Cloud database migration & initialization script
│   └── ui_app.py             # Streamlit dashboard interface & conversational UI
├── .gitignore
├── README.md
├── requirements.txt
└── schema.sql                # Relational database schema definitions
