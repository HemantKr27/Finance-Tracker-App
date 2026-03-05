from app.database.db import get_db_connection


def set_budget(user_id, category_id, amount, month, year):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM budgets
        WHERE user_id = ? AND category_id = ? AND month = ? AND year = ?
    """, (user_id, category_id, month, year))

    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE budgets
            SET amount = ?
            WHERE user_id = ? AND category_id = ? AND month = ? AND year = ?
        """, (amount, user_id, category_id, month, year))

    else:
        cursor.execute("""
            INSERT INTO budgets (user_id, category_id, amount, month, year)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, category_id, amount, month, year))

    conn.commit()
    conn.close()


def get_budget(user_id, category_id, month, year):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT amount
        FROM budgets
        WHERE user_id = ? AND category_id = ? AND month = ? AND year = ?
    """, (user_id, category_id, month, year))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result["amount"]

    return 0


def get_spent_amount(user_id, category_id, month, year):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE user_id = ?
        AND category_id = ?
        AND type = 'Expense'
        AND strftime('%m', date) = ?
        AND strftime('%Y', date) = ?
    """, (user_id, category_id, f"{month:02d}", str(year)))

    result = cursor.fetchone()

    conn.close()

    if result and result[0]:
        return result[0]

    return 0


def get_remaining_budget(user_id, category_id, month, year):

    budget = get_budget(user_id, category_id, month, year)
    spent = get_spent_amount(user_id, category_id, month, year)

    return budget - spent


def get_budget_status(user_id, category_id, month, year):

    budget = get_budget(user_id, category_id, month, year)

    if budget == 0:
        return {
            "budget": 0,
            "spent": 0,
            "remaining": 0,
            "percentage": 0,
            "status": "No Budget Set"
        }

    spent = get_spent_amount(user_id, category_id, month, year)

    remaining = budget - spent
    percentage = (spent / budget) * 100

    status = "OK"

    if percentage >= 100:
        status = "Exceeded"
    elif percentage >= 80:
        status = "Warning"

    return {
        "budget": budget,
        "spent": spent,
        "remaining": remaining,
        "percentage": percentage,
        "status": status
    }