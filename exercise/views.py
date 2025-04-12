from flask import Blueprint, request, jsonify
from .models import Exercise
from .database import get_all_exercises, create_exercise

bp = Blueprint('exercises', __name__, url_prefix='/exercises')

@bp.route('', methods=['GET'])
def get_exercises():
    exercises = get_all_exercises()
    return jsonify([{
        'id': ex.id,
        'type': ex.type,
        'muscle_group': ex.muscle_group,
        'info': ex.info
    } for ex in exercises])

@bp.route('', methods=['POST'])
def create_exercise_endpoint():
    data = request.get_json()
    
    if not all(key in data for key in ['type', 'muscle_group']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    exercise = Exercise.create(
        type=data['type'],
        muscle_group=data['muscle_group'],
        info=data.get('info')
    )
    
    create_exercise(exercise)
    
    return jsonify({
        'id': exercise.id,
        'type': exercise.type,
        'muscle_group': exercise.muscle_group,
        'info': exercise.info
    }), 201
