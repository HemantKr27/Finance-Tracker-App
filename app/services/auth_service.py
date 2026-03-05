import bcrypt
from app.database.db import get_db_connection


def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        cursor.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        conn.commit()
        conn.close()

        return True, "User registered successfully"

    except Exception as e:
        conn.close()
        return False, f"Registration failed: {str(e)}"


def authenticate_user(username, password):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode(), user["password_hash"]):
        return user["id"], user["username"]

    return None, None


def get_username(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()
    conn.close()

    return user["username"] if user else None