import sqlite3

DB_PATH = "data/budget.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Function to create a database connection
def get_db_connection():
    conn = sqlite3.connect("budget.db")
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn



