import sqlite3
import re

def parse_insert_statements(sql_file_path):
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract INSERT INTO statements for catbreeds and dogbreeds
    insert_pattern = re.compile(
        r"INSERT INTO (catbreeds|dogbreeds) \((.*?)\) VALUES\s*(.*?);",
        re.DOTALL | re.IGNORECASE
    )

    inserts = insert_pattern.findall(content)
    parsed_data = {'catbreeds': [], 'dogbreeds': []}

    for table, columns_str, values_str in inserts:
        # Clean columns list
        columns = [col.strip() for col in columns_str.split(',')]

        # Split values by '),(' but handle first and last parentheses
        values_str = values_str.strip()
        if values_str.startswith('(') and values_str.endswith(')'):
            values_str = values_str[1:-1]

        # Split individual records
        records = re.split(r"\),\s*\(", values_str)

        for record in records:
            # Split fields by comma, but commas inside quotes should be ignored
            fields = []
            current = ''
            in_quotes = False
            for char in record:
                if char == "'" and (not current or current[-1] != "\\"):
                    in_quotes = not in_quotes
                    current += char
                elif char == ',' and not in_quotes:
                    fields.append(current.strip())
                    current = ''
                else:
                    current += char
            if current:
                fields.append(current.strip())

            # Remove surrounding quotes from string fields
            cleaned_fields = []
            for field in fields:
                field = field.strip()
                if field.startswith("'") and field.endswith("'"):
                    field = field[1:-1].replace("\\'", "'")
                elif field.upper() == 'NULL':
                    field = None
                cleaned_fields.append(field)

            # Map columns to values
            record_dict = dict(zip(columns, cleaned_fields))
            parsed_data[table.lower()].append(record_dict)

    return parsed_data

def insert_data_to_db(db_path, data):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Insert catbreeds
    for record in data.get('catbreeds', []):
        placeholders = ', '.join(['?'] * len(record))
        columns = ', '.join(record.keys())
        values = tuple(record.values())
        try:
            cursor.execute(f"INSERT INTO catbreeds ({columns}) VALUES ({placeholders})", values)
        except Exception as e:
            print(f"Error inserting catbreeds record: {e}")

    # Insert dogbreeds
    for record in data.get('dogbreeds', []):
        placeholders = ', '.join(['?'] * len(record))
        columns = ', '.join(record.keys())
        values = tuple(record.values())
        try:
            cursor.execute(f"INSERT INTO dogbreeds ({columns}) VALUES ({placeholders})", values)
        except Exception as e:
            print(f"Error inserting dogbreeds record: {e}")

    conn.commit()
    conn.close()
    print("Data import completed.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python import_full_breed_data.py <path_to_sql_dump.sql> <path_to_sqlite_db.db>")
        sys.exit(1)

    sql_dump_path = sys.argv[1]
    sqlite_db_path = sys.argv[2]

    data = parse_insert_statements(sql_dump_path)
    insert_data_to_db(sqlite_db_path, data)
