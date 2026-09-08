# AI-Powered Inventory & Analytics Assistant

An intelligent full-stack conversational analytics dashboard that translates natural language business questions into executable SQL queries, fetches real-time data from a cloud MySQL database, and synthesizes direct operational insights using Google Gemini AI.

---

## Architecture Overview

* **User Query (Streamlit UI)**: Captures conversational business inquiries in plain English.
* **Gemini 3.5 Flash-Lite (Text-to-SQL)**: Converts natural language requests into schema-aware, optimized SQL queries.
* **Security Guardrail**: Verifies query safety, restricting execution strictly to read-only `SELECT` queries.
* **TiDB / Cloud MySQL Database**: Executes verified queries against production tables (`products`, `categories`, `orders`, `order_items`).
* **Gemini 3.5 Flash-Lite (Summarizer)**: Ingests raw tabular output and generates executive, human-readable insights.
* **Streamlit Interactive Interface**: Renders the complete conversation history with SQL cards, interactive dataframes, and analytical summaries.

---

## Features

* **Natural Language to SQL**: Converts ad-hoc conversational inquiries into optimized SQL queries instantly.
* **Query Safety Guardrails**: Restricts execution strictly to read-only (`SELECT`) queries to prevent accidental modifications or destructive commands (`DROP`, `DELETE`, `UPDATE`).
* **Cloud Database Connectivity**: Directly queries remote TiDB / MySQL instances using `mysql-connector-python`.
* **Dynamic Table Rendering**: Parses database cursor responses dynamically into tabular format with Pandas and Streamlit.
* **Dual LLM Pipeline**: Uses distinct prompt engineering workflows for accurate schema-based SQL translation and natural language business summarization.
* **Database Explorer**: Integrated sidebar component allowing users to inspect raw records from any table on demand.

---

## Tech Stack

* **Frontend & UI**: Streamlit
* **LLM Engine**: Google Gemini API (`gemini-3.5-flash-lite`)
* **Database**: TiDB Cloud (MySQL 8.0 compatible)
* **Backend & Data Processing**: Python 3.11+, Pandas, `mysql-connector-python`
* **Deployment**: Streamlit Community Cloud

---

## Project Structure

```text
ai-inventory-assistant/
├── src/
│   ├── ai_service.py       # Gemini API client, schema prompts, SQL safety validation
│   ├── db.py               # MySQL/TiDB database connection and query executor
│   ├── ui_app.py           # Streamlit dashboard interface and chat orchestrator
│   └── app.py              # Terminal/CLI version of the assistant
├── requirements.txt        # Production Python dependencies
└── README.md               # Project documentation




Local Setup & Installation
1. Clone the Repository
Bash
git clone [https://github.com/muskanlalwani155-design/ai-inventory-assistant.git](https://github.com/muskanlalwani155-design/ai-inventory-assistant.git)
cd ai-inventory-assistant

2. Create and Activate Virtual Environment
Bash
python -m venv venv
Windows:

Bash
venv\Scripts\activate
macOS / Linux:

Bash
source venv/bin/activate

3. Install Dependencies
Bash
pip install -r requirements.txt

4. Configure Secrets
Create a directory .streamlit and add a secrets.toml file inside it:

Ini, TOML
DB_HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
DB_PORT = 4000
DB_USER = "your_db_username"
DB_PASSWORD = "your_db_password"
DB_NAME = "inventory_db"
GEMINI_API_KEY = "your_gemini_api_key"

5. Run the Application
Bash
streamlit run src/ui_app.py
Deployment (Streamlit Cloud)
Push your code to your GitHub repository.

Sign in to Streamlit Community Cloud.
Click Create app and select your repository.
Set the Main file path to src/ui_app.py.
Open Advanced settings → Secrets and paste your database credentials and GEMINI_API_KEY.
Click Deploy.