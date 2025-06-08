import sqlite3
import re

def convert_mariadb_to_sqlite(sql_dump_path: str, sqlite_db_path: str):
    with open(sql_dump_path, 'r', encoding='utf-8') as f:
        sql_dump = f.read()

    # Remove or replace MariaDB/MySQL specific syntax for SQLite compatibility
    # Remove backticks
    sql_dump = sql_dump.replace('`', '')

    # Remove ENGINE and CHARSET specifications
    sql_dump = re.sub(r'ENGINE=\\w+\\s*DEFAULT CHARSET=\\w+\\s*COLLATE=\\w+;', '', sql_dump, flags=re.IGNORECASE)
    sql_dump = re.sub(r'ENGINE=\\w+;', '', sql_dump, flags=re.IGNORECASE)

    # Remove AUTO_INCREMENT syntax (SQLite uses AUTOINCREMENT)
    sql_dump = re.sub(r'AUTO_INCREMENT=\\d+;', '', sql_dump, flags=re.IGNORECASE)

    # Replace AUTO_INCREMENT with AUTOINCREMENT
    sql_dump = re.sub(r'NOT NULL AUTO_INCREMENT', 'INTEGER PRIMARY KEY AUTOINCREMENT', sql_dump, flags=re.IGNORECASE)

    # Remove /*!40101 ... */ comments
    sql_dump = re.sub(r'/\\*!\\d+ .*? \\*/;', '', sql_dump, flags=re.DOTALL)

    # Remove SET statements and transaction commands
    sql_dump = re.sub(r'SET .*?;', '', sql_dump)
    sql_dump = re.sub(r'START TRANSACTION;', '', sql_dump)
    sql_dump = re.sub(r'COMMIT;', '', sql_dump)

    # Remove timestamp default current_timestamp() ON UPDATE current_timestamp()
    sql_dump = re.sub(r'DEFAULT current_timestamp\\(\\) ON UPDATE current_timestamp\\(\\)', 'DEFAULT CURRENT_TIMESTAMP', sql_dump, flags=re.IGNORECASE)

    # Remove COLLATE specifications in columns
    sql_dump = re.sub(r'COLLATE \\w+', '', sql_dump, flags=re.IGNORECASE)

    # Remove comments starting with --
    sql_dump = re.sub(r'--.*?\\n', '', sql_dump)

    # Remove empty lines
    sql_dump = '\\n'.join([line for line in sql_dump.splitlines() if line.strip() != ''])

    # Split the SQL dump into individual statements
    statements = [stmt.strip() for stmt in sql_dump.split(';') if stmt.strip()]

    conn = sqlite3.connect(sqlite_db_path)
    cursor = conn.cursor()

    try:
        for stmt in statements:
            try:
                cursor.execute(stmt)
            except sqlite3.Error as e:
                print(f"SQLite error executing statement: {e}\nStatement: {stmt}")
        conn.commit()
        print(f"Successfully imported SQL dump into {sqlite_db_path}")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python convert_sql_dump_to_sqlite.py <mariadb_sql_dump.sql> <output_sqlite_db.db>")
        sys.exit(1)

    sql_dump_path = sys.argv[1]
    sqlite_db_path = sys.argv[2]

    convert_mariadb_to_sqlite(sql_dump_path, sqlite_db_path)
