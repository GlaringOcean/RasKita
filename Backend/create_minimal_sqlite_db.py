import sqlite3

def create_minimal_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create catbreeds table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS catbreeds (
        cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        breed_name TEXT NOT NULL,
        height_male_min REAL NOT NULL,
        height_male_max REAL NOT NULL,
        height_female_min REAL NOT NULL,
        height_female_max REAL NOT NULL,
        weight_male_min REAL NOT NULL,
        weight_male_max REAL NOT NULL,
        weight_female_min REAL NOT NULL,
        weight_female_max REAL NOT NULL,
        life_expectancy_min INTEGER NOT NULL,
        life_expectancy_max INTEGER NOT NULL,
        characteristics TEXT NOT NULL,
        exercise_needs TEXT NOT NULL,
        grooming_requirements TEXT NOT NULL,
        health_considerations TEXT NOT NULL,
        diet_nutrition TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert sample data into catbreeds
    cursor.execute("""
    INSERT INTO catbreeds (
        breed_name, height_male_min, height_male_max, height_female_min, height_female_max,
        weight_male_min, weight_male_max, weight_female_min, weight_female_max,
        life_expectancy_min, life_expectancy_max, characteristics, exercise_needs,
        grooming_requirements, health_considerations, diet_nutrition
    ) VALUES (
        'Abyssinian', 8.0, 10.0, 8.0, 10.0,
        7.0, 12.0, 6.0, 9.0,
        14, 17, 'Friendly, interactive, animated, active, and playful',
        'Requires ample playtime and mental stimulation',
        'Minimal grooming due to short coat; regular brushing helps maintain coat health',
        'Regular veterinary check-ups are important',
        'Balanced diet essential; monitor food intake to prevent overeating'
    )
    """)

    # Create dogbreeds table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dogbreeds (
        dog_id INTEGER PRIMARY KEY AUTOINCREMENT,
        breed_name TEXT NOT NULL,
        height_male_min REAL NOT NULL,
        height_male_max REAL NOT NULL,
        height_female_min REAL NOT NULL,
        height_female_max REAL NOT NULL,
        weight_male_min REAL NOT NULL,
        weight_male_max REAL NOT NULL,
        weight_female_min REAL NOT NULL,
        weight_female_max REAL NOT NULL,
        life_expectancy_min INTEGER NOT NULL,
        life_expectancy_max INTEGER NOT NULL,
        characteristics TEXT NOT NULL,
        exercise_needs TEXT NOT NULL,
        grooming_requirements TEXT NOT NULL,
        health_considerations TEXT NOT NULL,
        diet_nutrition TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Insert sample data into dogbreeds
    cursor.execute("""
    INSERT INTO dogbreeds (
        breed_name, height_male_min, height_male_max, height_female_min, height_female_max,
        weight_male_min, weight_male_max, weight_female_min, weight_female_max,
        life_expectancy_min, life_expectancy_max, characteristics, exercise_needs,
        grooming_requirements, health_considerations, diet_nutrition
    ) VALUES (
        'Alaskan Malamute', 25.0, 25.0, 23.0, 23.0,
        85.0, 85.0, 75.0, 75.0,
        10, 14, 'Affectionate, Loyal, Playful, Dignified, Friendly, Devoted',
        'High energy; needs daily vigorous exercise like hiking, running, or pulling sleds',
        'Thick double coat needs frequent brushing, especially during shedding seasons. Bathe occasionally',
        'Generally healthy but can have hip dysplasia and inherited diseases. Regular vet checks recommended',
        'Feed high-quality dog food suited for large, active breeds. Monitor weight and avoid overfeeding'
    )
    """)

    conn.commit()
    conn.close()
    print(f"Minimal SQLite database created at {db_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python create_minimal_sqlite_db.py <output_sqlite_db.db>")
        sys.exit(1)
    db_path = sys.argv[1]
    create_minimal_db(db_path)
