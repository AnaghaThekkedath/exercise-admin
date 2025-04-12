import pytest
from exercise.models import Exercise

def test_create_exercise(client, sample_exercise):
    """Test creating a new exercise"""
    response = client.post('/exercises/', json=sample_exercise)
    assert response.status_code == 201
    data = response.get_json()
    assert data['type'] == sample_exercise['type']
    assert data['name'] == sample_exercise['name']
    assert data['muscle_group'] == sample_exercise['muscle_group']
    assert data['info'] == sample_exercise['info']
    assert 'id' in data

def test_get_exercises_empty(client):
    """Test getting exercises when none exist"""
    response = client.get('/exercises/')
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_exercises(client, sample_exercise):
    """Test getting all exercises"""
    # Create an exercise first
    client.post('/exercises/', json=sample_exercise)
    
    response = client.get('/exercises/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['type'] == sample_exercise['type']
    assert data[0]['name'] == sample_exercise['name']

def test_create_exercise_missing_fields(client):
    """Test creating an exercise with missing required fields"""
    # Missing type
    response = client.post('/exercises/', json={
        "name": "Bench Press",
        "muscle_group": "chest"
    })
    assert response.status_code == 400

    # Missing name
    response = client.post('/exercises/', json={
        "type": "strength",
        "muscle_group": "chest"
    })
    assert response.status_code == 400

    # Missing muscle_group
    response = client.post('/exercises/', json={
        "type": "strength",
        "name": "Bench Press"
    })
    assert response.status_code == 400

def test_create_exercise_optional_fields(client):
    """Test creating an exercise with optional fields"""
    exercise_data = {
        "type": "strength",
        "name": "Bench Press",
        "muscle_group": "chest"
    }
    response = client.post('/exercises/', json=exercise_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['info'] is None

    exercise_data['info'] = "Some info"
    response = client.post('/exercises/', json=exercise_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['info'] == "Some info" 