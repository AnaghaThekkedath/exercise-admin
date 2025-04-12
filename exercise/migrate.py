import sqlite3

def migrate():
    conn = sqlite3.connect('exercises.db')
    cursor = conn.cursor()
    
    # Check if the name column exists in exercises table
    cursor.execute("PRAGMA table_info(exercises)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'name' not in columns:
        # Add the name column with a default value
        cursor.execute('''
            ALTER TABLE exercises 
            ADD COLUMN name TEXT NOT NULL DEFAULT 'Unnamed Exercise'
        ''')
        print("Added 'name' column to exercises table")
    
    # Check if the program_exercises table exists and has the new columns
    cursor.execute("PRAGMA table_info(program_exercises)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'sets' not in columns:
        # Create a new table with the updated schema
        cursor.execute('''
            CREATE TABLE program_exercises_new (
                program_id TEXT,
                exercise_id TEXT,
                sets INTEGER NOT NULL DEFAULT 3,
                reps INTEGER,
                weight REAL,
                FOREIGN KEY (program_id) REFERENCES programs (id),
                FOREIGN KEY (exercise_id) REFERENCES exercises (id),
                PRIMARY KEY (program_id, exercise_id)
            )
        ''')
        
        # Copy data from old table to new table
        cursor.execute('''
            INSERT INTO program_exercises_new (program_id, exercise_id, sets)
            SELECT program_id, exercise_id, 3
            FROM program_exercises
        ''')
        
        # Drop old table and rename new table
        cursor.execute('DROP TABLE program_exercises')
        cursor.execute('ALTER TABLE program_exercises_new RENAME TO program_exercises')
        print("Updated program_exercises table with new columns")
    
    conn.commit()
    conn.close()
    print("Migration completed successfully")

if __name__ == '__main__':
    migrate() 