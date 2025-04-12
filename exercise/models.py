# stores the models for the appliction

from dataclasses import dataclass
from typing import Optional, List
import uuid
from flask_restx import fields

@dataclass
class Exercise:
    id: str
    type: str
    name: str
    muscle_group: str
    info: Optional[str] = None

    @classmethod
    def create(cls, type: str, name: str, muscle_group: str, info: Optional[str] = None) -> 'Exercise':
        return cls(
            id=str(uuid.uuid4()),
            type=type,
            name=name,
            muscle_group=muscle_group,
            info=info
        )

@dataclass
class Program:
    id: str
    name: str
    description: Optional[str] = None
    exercises: List[str] = None  # List of exercise IDs

    @classmethod
    def create(cls, name: str, description: Optional[str] = None, exercises: List[str] = None) -> 'Program':
        return cls(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            exercises=exercises or []
        )

@dataclass
class ProgramExercise:
    exercise_id: str
    program_id: str
    sets: int
    reps: Optional[int] = None
    weight: Optional[float] = None

    @classmethod
    def create(cls, exercise_id: str, program_id: str, sets: int, reps: Optional[int] = None, weight: Optional[float] = None) -> 'ProgramExercise':
        return cls(
            exercise_id=exercise_id,
            program_id=program_id,
            sets=sets,
            reps=reps,
            weight=weight
        )

def create_api_models(api):
    exercise_model = api.model('Exercise', {
        'id': fields.String(readonly=True, description='The exercise unique identifier'),
        'type': fields.String(required=True, description='The type of exercise'),
        'name': fields.String(required=True, description='The name of the exercise'),
        'muscle_group': fields.String(required=True, description='The muscle group targeted'),
        'info': fields.String(description='Additional information about the exercise')
    })

    exercise_input_model = api.model('ExerciseInput', {
        'type': fields.String(required=True, description='The type of exercise'),
        'name': fields.String(required=True, description='The name of the exercise'),
        'muscle_group': fields.String(required=True, description='The muscle group targeted'),
        'info': fields.String(description='Additional information about the exercise')
    })

    program_model = api.model('Program', {
        'id': fields.String(readonly=True, description='The program unique identifier'),
        'name': fields.String(required=True, description='The name of the program'),
        'description': fields.String(description='Description of the program'),
        'exercises': fields.List(fields.String, description='List of exercise IDs in the program')
    })

    program_input_model = api.model('ProgramInput', {
        'name': fields.String(required=True, description='The name of the program'),
        'description': fields.String(description='Description of the program'),
        'exercises': fields.List(fields.String, description='List of exercise IDs in the program')
    })

    program_exercise_model = api.model('ProgramExercise', {
        'exercise_id': fields.String(required=True, description='The exercise ID'),
        'program_id': fields.String(required=True, description='The program ID'),
        'sets': fields.Integer(required=True, description='The number of sets'),
        'reps': fields.Integer(description='The number of reps'),
        'weight': fields.Float(description='The weight lifted')
    })

    return exercise_model, exercise_input_model, program_model, program_input_model, program_exercise_model