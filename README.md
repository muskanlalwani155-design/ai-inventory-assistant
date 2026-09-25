# AI-Powered Inventory & Analytics Assistant

An intelligent full-stack conversational analytics dashboard that translates natural language business questions into executable SQL queries, fetches real-time data from a cloud MySQL database, and synthesizes direct operational insights using Google Gemini AI.

---

## 🛠️ Tech Stack

* **Frontend & Dashboard UI**: Streamlit
* **AI & LLM Engine**: Google Gemini API (`GEMINI_API_KEY`, prompt-engineered Text-to-SQL & summarization)
* **Data Processing & Manipulation**: Pandas, Python 3.11+
* **Database & Cloud Storage**: TiDB Cloud (Serverless MySQL 8.0 compatible)
* **Database Connector**: `mysql-connector-python`
* **Deployment Platform**: Streamlit Community Cloud

---

## 🏗️ Architecture Overview

* **User Query (Streamlit UI)**: Captures conversational business inquiries in plain English.
* **Google Gemini API (Text-to-SQL)**: Converts natural language requests into schema-aware, optimized SQL queries.
* **Security Guardrail**: Verifies query safety, restricting execution strictly to safe, read-only `SELECT` queries.
* **TiDB / Cloud MySQL Database**: Executes verified queries against production tables (`products`, `categories`, `orders`, `order_items`).
* **Google Gemini API (Summarizer)**: Ingests raw tabular output and generates executive, human-readable insights.
* **Streamlit Interactive Interface**: Renders the complete conversation history with SQL cards, interactive dataframes, and analytical summaries.

---

## ✨ Features

* **Natural Language to SQL**: Converts ad-hoc conversational inquiries into optimized SQL queries instantly.
* **Query Safety Guardrails**: Restricts execution strictly to read-only (`SELECT`) queries to prevent accidental modifications or destructive commands (`DROP`, `DELETE`, `UPDATE`).
* **Cloud Database Connectivity**: Directly queries remote TiDB / MySQL instances using `mysql-connector-python`.
* **Dynamic Table Rendering**: Parses database cursor responses dynamically into clean tabular formats with Pandas and Streamlit.
* **Dual LLM Pipeline**: Uses distinct prompt engineering workflows for accurate schema-based SQL translation and natural language business summarization.
* **Database Explorer**: Integrated sidebar component allowing users to inspect raw records from any table on demand.

---

## 📁 Project Structure

```text
ai-inventory-assistant/
├── src/
│   ├── ai_service.py       # Gemini API client, schema prompts, SQL safety validation
│   ├── db.py               # MySQL/TiDB database connection and query executor
│   ├── ui_app.py           # Streamlit dashboard interface and chat orchestrator
│   └── app.py              # Terminal/CLI version of the assistant
├── requirements.txt        # Production Python dependencies
└── README.md               # Project documentation
