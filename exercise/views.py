from flask import request
from flask_restx import Resource, Api, Namespace
from .models import Exercise, Program, create_api_models
from .database import (
    get_all_exercises, create_exercise,
    get_all_programs, get_program, create_program, update_program
)

# Create namespaces for our API
exercises_api = Namespace('exercises', description='Exercise operations')
programs_api = Namespace('programs', description='Program operations')

# Create API models
exercise_model, exercise_input_model, program_model, program_input_model, _ = create_api_models(exercises_api)

# Exercise endpoints
@exercises_api.route('/')
class ExerciseList(Resource):
    @exercises_api.doc('list_exercises')
    @exercises_api.marshal_list_with(exercise_model)
    def get(self):
        """List all exercises"""
        return get_all_exercises()

    @exercises_api.doc('create_exercise')
    @exercises_api.expect(exercise_input_model)
    @exercises_api.marshal_with(exercise_model, code=201)
    def post(self):
        """Create a new exercise"""
        data = request.get_json()
        
        if not all(key in data for key in ['type', 'muscle_group', 'name']):
            exercises_api.abort(400, 'Missing required fields')
        
        exercise = Exercise.create(
            type=data['type'],
            name=data['name'],
            muscle_group=data['muscle_group'],
            info=data.get('info')
        )
        
        create_exercise(exercise)
        
        return exercise, 201

# Program endpoints
@programs_api.route('/')
class ProgramList(Resource):
    @programs_api.doc('list_programs')
    @programs_api.marshal_list_with(program_model)
    def get(self):
        """List all programs"""
        return get_all_programs()

    @programs_api.doc('create_program')
    @programs_api.expect(program_input_model)
    @programs_api.marshal_with(program_model, code=201)
    def post(self):
        """Create a new program"""
        data = request.get_json()
        
        if 'name' not in data:
            programs_api.abort(400, 'Name is required')
        
        program = Program.create(
            name=data['name'],
            description=data.get('description'),
            exercises=data.get('exercises', [])
        )
        
        create_program(program)
        
        return program, 201

@programs_api.route('/<string:program_id>')
@programs_api.param('program_id', 'The program identifier')
class ProgramResource(Resource):
    @programs_api.doc('get_program')
    @programs_api.marshal_with(program_model)
    def get(self, program_id):
        """Get a program by its ID"""
        program = get_program(program_id)
        if program is None:
            programs_api.abort(404, f'Program {program_id} not found')
        return program

    @programs_api.doc('update_program')
    @programs_api.expect(program_input_model)
    @programs_api.marshal_with(program_model)
    def put(self, program_id):
        """Update a program"""
        program = get_program(program_id)
        if program is None:
            programs_api.abort(404, f'Program {program_id} not found')
        
        data = request.get_json()
        if 'name' not in data:
            programs_api.abort(400, 'Name is required')
        
        updated_program = Program(
            id=program_id,
            name=data['name'],
            description=data.get('description'),
            exercises=data.get('exercises', [])
        )
        
        update_program(updated_program)
        
        return updated_program

        
