from app.database.db import get_db_connection
import pandas as pd


# Function to add a transaction
def add_transaction(user_id, category, amount, type_, date, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_id, category, amount, type, date, description) 
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, category, amount, type_, date, description))
    conn.commit()
    conn.close()


# Function to update a transaction
def update_transaction(transaction_id, category, amount, type_, date, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE transactions 
        SET category = ?, amount = ?, type = ?, date = ?, description = ? 
        WHERE id = ?
    """, (category, amount, type_, date, description, transaction_id))
    conn.commit()


# Function to delete a transaction
def delete_transaction(transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    conn.commit()


# Function to fetch transactions for a user
def get_transactions(user_id, start_date=None, end_date=None, category=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id, category, type, amount, date, description FROM transactions WHERE user_id = ? AND type = 'Expense'"
    params = [user_id]

    if start_date:
        query += " AND date >= ?"
        params.append(start_date)
    if end_date:
        query += " AND date <= ?"
        params.append(end_date)
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    df = pd.read_sql_query(query, conn, params=params)
    return df

# Function to calculate net savings
def calculate_net_savings(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END) AS total_income,
            SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END) AS total_expense
        FROM transactions WHERE user_id = ?
    """, (user_id,))
    result = cursor.fetchone()
    income = result[0] if result[0] else 0
    expense = result[1] if result[1] else 0
    return income, expense, income - expense