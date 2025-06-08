import sqlite3
import sys

def list_tables(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print("Tables in database:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("No tables found in the database.")
        conn.close()
    except Exception as e:
        print(f"Error accessing database: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_sqlite_tables.py <path_to_sqlite_db>")
        sys.exit(1)
    db_path = sys.argv[1]
    list_tables(db_path)
