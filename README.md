# AI-Powered Smart Inventory & SQL Analytics Assistant

An enterprise backend system built with Python, MySQL, and Google Gemini API. It handles transactional order processing with ACID compliance and provides a natural-language Text-to-SQL analytics engine.

## Features
- **ACID Transaction Management:** Implements row-level locking (`SELECT ... FOR UPDATE`), rollbacks, and atomic multi-table updates during order placement.
- **Natural Language to SQL:** Uses Gemini 2.5/3.6 models to translate human business questions into optimized MySQL `JOIN` and aggregation queries.
- **Security Guardrails:** Validates generated queries against destructive SQL statements (`DROP`, `DELETE`, `UPDATE`) to enforce read-only analytical execution.
- **Relational Architecture:** Fully normalized MySQL schema covering products, categories, orders, and order items.

## Tech Stack
- **Language:** Python 3.10+
- **Database:** MySQL 8.0+
- **AI Integration:** Google GenAI SDK (Gemini API)
- **Database Driver:** mysql-connector-python

## Database Schema
- `categories` (category_id, category_name)
- `products` (product_id, product_name, category_id, price, stock_quantity)
- `orders` (order_id, customer_name, order_date, total_amount)
- `order_items` (order_item_id, order_id, product_id, quantity, unit_price)

## Setup & Installation
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd ai-inventory-assistant



1.Activate virtual environment and install dependencies:

Bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

====================================================

2.Configure .env file:

Code snippet
DB_HOST=localhost
DB_PORT=3307
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=inventory_db
GEMINI_API_KEY=your_gemini_key

=====================================================

3.Run Database Schema:
Import schema.sql into MySQL Workbench or CLI.

======================================================

4.Run the assistant:

Bash
python src/app.py



