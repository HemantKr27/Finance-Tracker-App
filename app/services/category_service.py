from app.database.db import get_db_connection


def get_categories():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM categories")

    rows = cursor.fetchall()

    conn.close()

    return rows