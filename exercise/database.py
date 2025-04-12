import sqlite3
from typing import List, Optional
from .models import Exercise, Program, ProgramExercise

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            name TEXT NOT NULL,
            muscle_group TEXT NOT NULL,
            info TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS programs (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS program_exercises (
            program_id TEXT,
            exercise_id TEXT,
            sets INTEGER NOT NULL,
            reps INTEGER,
            weight REAL,
            FOREIGN KEY (program_id) REFERENCES programs (id),
            FOREIGN KEY (exercise_id) REFERENCES exercises (id),
            PRIMARY KEY (program_id, exercise_id)
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('exercises.db')
    conn.row_factory = sqlite3.Row
    return conn

# Exercise operations
def get_all_exercises() -> List[Exercise]:
    conn = get_db_connection()
    exercises = conn.execute('SELECT * FROM exercises').fetchall()
    conn.close()
    return [Exercise(
        id=ex['id'],
        type=ex['type'],
        name=ex['name'],
        muscle_group=ex['muscle_group'],
        info=ex['info']
    ) for ex in exercises]

def get_exercise(exercise_id: str) -> Optional[Exercise]:
    conn = get_db_connection()
    exercise = conn.execute('SELECT * FROM exercises WHERE id = ?', (exercise_id,)).fetchone()
    conn.close()
    if exercise:
        return Exercise(
            id=exercise['id'],
            type=exercise['type'],
            name=exercise['name'],
            muscle_group=exercise['muscle_group'],
            info=exercise['info']
        )
    return None

def create_exercise(exercise: Exercise) -> None:
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO exercises (id, type, name, muscle_group, info) VALUES (?, ?, ?, ?, ?)',
        (exercise.id, exercise.type, exercise.name, exercise.muscle_group, exercise.info)
    )
    conn.commit()
    conn.close()

# Program operations
def get_all_programs() -> List[Program]:
    conn = get_db_connection()
    programs = conn.execute('SELECT * FROM programs').fetchall()
    result = []
    for program in programs:
        exercises = conn.execute(
            'SELECT exercise_id, sets, reps, weight FROM program_exercises WHERE program_id = ?',
            (program['id'],)
        ).fetchall()
        result.append(Program(
            id=program['id'],
            name=program['name'],
            description=program['description'],
            exercises=[ex['exercise_id'] for ex in exercises]
        ))
    conn.close()
    return result

def get_program(program_id: str) -> Optional[Program]:
    conn = get_db_connection()
    program = conn.execute('SELECT * FROM programs WHERE id = ?', (program_id,)).fetchone()
    if program:
        exercises = conn.execute(
            'SELECT exercise_id, sets, reps, weight FROM program_exercises WHERE program_id = ?',
            (program_id,)
        ).fetchall()
        result = Program(
            id=program['id'],
            name=program['name'],
            description=program['description'],
            exercises=[ex['exercise_id'] for ex in exercises]
        )
        conn.close()
        return result
    conn.close()
    return None

def create_program(program: Program) -> None:
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO programs (id, name, description) VALUES (?, ?, ?)',
        (program.id, program.name, program.description)
    )
    for exercise_id in program.exercises:
        conn.execute(
            'INSERT INTO program_exercises (program_id, exercise_id, sets) VALUES (?, ?, ?)',
            (program.id, exercise_id, 3)  # Default to 3 sets
        )
    conn.commit()
    conn.close()

def update_program(program: Program) -> None:
    conn = get_db_connection()
    conn.execute(
        'UPDATE programs SET name = ?, description = ? WHERE id = ?',
        (program.name, program.description, program.id)
    )
    conn.execute('DELETE FROM program_exercises WHERE program_id = ?', (program.id,))
    for exercise_id in program.exercises:
        conn.execute(
            'INSERT INTO program_exercises (program_id, exercise_id, sets) VALUES (?, ?, ?)',
            (program.id, exercise_id, 3)  # Default to 3 sets
        )
    conn.commit()
    conn.close() 