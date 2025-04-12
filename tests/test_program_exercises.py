import pytest

def test_create_program_with_exercises(client, sample_exercise, sample_program):
    """Test creating a program with exercises"""
    # Create an exercise first
    exercise_response = client.post('/exercises/', json=sample_exercise)
    exercise_id = exercise_response.get_json()['id']
    
    # Create a program with the exercise
    program_data = sample_program.copy()
    program_data['exercises'] = [exercise_id]
    
    response = client.post('/programs/', json=program_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['exercises'] == [exercise_id]

def test_update_program_exercises(client, sample_exercise, sample_program):
    """Test updating a program's exercises"""
    # Create two exercises
    exercise1_response = client.post('/exercises/', json=sample_exercise)
    exercise1_id = exercise1_response.get_json()['id']
    
    exercise2_data = sample_exercise.copy()
    exercise2_data['name'] = "Squat"
    exercise2_response = client.post('/exercises/', json=exercise2_data)
    exercise2_id = exercise2_response.get_json()['id']
    
    # Create a program with one exercise
    program_data = sample_program.copy()
    program_data['exercises'] = [exercise1_id]
    program_response = client.post('/programs/', json=program_data)
    program_id = program_response.get_json()['id']
    
    # Update the program with both exercises
    update_data = {
        "name": program_data['name'],
        "description": program_data['description'],
        "exercises": [exercise1_id, exercise2_id]
    }
    response = client.put(f'/programs/{program_id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['exercises']) == 2
    assert exercise1_id in data['exercises']
    assert exercise2_id in data['exercises']

def test_program_with_nonexistent_exercise(client, sample_program):
    """Test creating a program with a nonexistent exercise"""
    program_data = sample_program.copy()
    program_data['exercises'] = ['nonexistent-exercise-id']
    
    response = client.post('/programs/', json=program_data)
    assert response.status_code == 201  # Should still create the program
    data = response.get_json()
    assert data['exercises'] == ['nonexistent-exercise-id']  # The exercise ID is stored but not validated 