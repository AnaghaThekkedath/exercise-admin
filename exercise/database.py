import sqlite3
from typing import List
from .models import Exercise

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            muscle_group TEXT NOT NULL,
            info TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('exercises.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_all_exercises() -> List[Exercise]:
    conn = get_db_connection()
    exercises = conn.execute('SELECT * FROM exercises').fetchall()
    conn.close()
    return [Exercise(
        id=ex['id'],
        type=ex['type'],
        muscle_group=ex['muscle_group'],
        info=ex['info']
    ) for ex in exercises]

def create_exercise(exercise: Exercise) -> None:
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO exercises (id, type, muscle_group, info) VALUES (?, ?, ?, ?)',
        (exercise.id, exercise.type, exercise.muscle_group, exercise.info)
    )
    conn.commit()
    conn.close() 