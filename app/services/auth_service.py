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
        "SELECT id, password_hash FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        stored_hash = user["password_hash"]

        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return user["id"]

    return None