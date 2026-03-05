from app.database.db import get_db_connection
import pandas as pd


# -----------------------------
# Add Transaction
# -----------------------------
def add_transaction(user_id, category_id, amount, type_, date, description):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions 
        (user_id, category_id, amount, type, date, description)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, category_id, amount, type_, date, description))

    conn.commit()
    conn.close()


# -----------------------------
# Update Transaction
# -----------------------------
def update_transaction(transaction_id, category_id, amount, type_, date, description):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET category_id = ?, amount = ?, type = ?, date = ?, description = ?
        WHERE id = ?
    """, (category_id, amount, type_, date, description, transaction_id))

    conn.commit()
    conn.close()


# -----------------------------
# Delete Transaction
# -----------------------------
def delete_transaction(transaction_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    conn.commit()
    conn.close()


# -----------------------------
# Get Transactions
# -----------------------------
def get_transactions(user_id, start_date=None, end_date=None, category_id=None):

    conn = get_db_connection()

    query = """
        SELECT 
            t.id,
            c.name AS category,
            t.type,
            t.amount,
            t.date,
            t.description
        FROM transactions t
        JOIN categories c
        ON t.category_id = c.id
        WHERE t.user_id = ?
    """

    params = [user_id]

    if start_date:
        query += " AND t.date >= ?"
        params.append(start_date)

    if end_date:
        query += " AND t.date <= ?"
        params.append(end_date)

    if category_id and category_id != "All":
        query += " AND t.category_id = ?"
        params.append(category_id)

    query += " ORDER BY t.date DESC"

    df = pd.read_sql_query(query, conn, params=params)

    conn.close()

    return df


# -----------------------------
# Net Savings Calculation
# -----------------------------
def calculate_net_savings(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END),
            SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END)
        FROM transactions
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()

    conn.close()

    income = result[0] if result[0] else 0
    expense = result[1] if result[1] else 0

    return income, expense, income - expense


# -----------------------------
# Spending by Category (Analytics)
# -----------------------------
def get_spending_by_category(user_id):

    conn = get_db_connection()

    query = """
        SELECT 
            c.name AS category,
            SUM(t.amount) AS total
        FROM transactions t
        JOIN categories c
        ON t.category_id = c.id
        WHERE t.user_id = ?
        AND t.type = 'Expense'
        GROUP BY c.name
    """

    df = pd.read_sql_query(query, conn, params=[user_id])

    conn.close()

    return df


# -----------------------------
# Monthly Spending
# -----------------------------
def get_monthly_spending(user_id):

    conn = get_db_connection()

    query = """
        SELECT 
            strftime('%Y-%m', date) AS month,
            SUM(amount) AS total
        FROM transactions
        WHERE user_id = ?
        AND type = 'Expense'
        GROUP BY month
        ORDER BY month
    """

    df = pd.read_sql_query(query, conn, params=[user_id])

    conn.close()

    return df