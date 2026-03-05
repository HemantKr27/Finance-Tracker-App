from app.database.db import get_db_connection

# Create Users table
def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash BLOB NOT NULL,
        email TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,

        amount REAL NOT NULL,
        type TEXT NOT NULL,

        description TEXT,
        date TEXT NOT NULL,

        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,

        amount REAL NOT NULL,

        month INTEGER NOT NULL,
        year INTEGER NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(category_id) REFERENCES categories(id),

        UNIQUE(user_id, category_id, month, year)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
    )
    """)

    seed_categories()
    conn.commit()
    conn.close()



def seed_categories():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]

        if count == 0:
            cursor.executemany(
                "INSERT INTO categories (name) VALUES (?)",
                [
                    ("Food",),
                    ("Entertainment",),
                    ("Bills",),
                    ("Shopping",),
                    ("Transport",),
                    ("Other",)
                ]
            )

        conn.commit()
        conn.close()
