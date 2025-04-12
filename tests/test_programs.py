import pytest

def test_create_program(client, sample_program):
    """Test creating a new program"""
    response = client.post('/programs/', json=sample_program)
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == sample_program['name']
    assert data['description'] == sample_program['description']
    assert data['exercises'] == sample_program['exercises']
    assert 'id' in data

def test_get_programs_empty(client):
    """Test getting programs when none exist"""
    response = client.get('/programs/')
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_programs(client, sample_program):
    """Test getting all programs"""
    # Create a program first
    client.post('/programs/', json=sample_program)
    
    response = client.get('/programs/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['name'] == sample_program['name']

def test_create_program_missing_fields(client):
    """Test creating a program with missing required fields"""
    # Missing name
    response = client.post('/programs/', json={
        "description": "A workout program",
        "exercises": []
    })
    assert response.status_code == 400

def test_create_program_optional_fields(client):
    """Test creating a program with optional fields"""
    program_data = {
        "name": "Workout Program"
    }
    response = client.post('/programs/', json=program_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['description'] is None
    assert data['exercises'] == []

    program_data['description'] = "Some description"
    program_data['exercises'] = []
    response = client.post('/programs/', json=program_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['description'] == "Some description"
    assert data['exercises'] == []

def test_get_program(client, sample_program):
    """Test getting a specific program"""
    # Create a program first
    create_response = client.post('/programs/', json=sample_program)
    program_id = create_response.get_json()['id']
    
    response = client.get(f'/programs/{program_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == sample_program['name']
    assert data['id'] == program_id

def test_get_nonexistent_program(client):
    """Test getting a program that doesn't exist"""
    response = client.get('/programs/nonexistent-id')
    assert response.status_code == 404

def test_update_program(client, sample_program):
    """Test updating a program"""
    # Create a program first
    create_response = client.post('/programs/', json=sample_program)
    program_id = create_response.get_json()['id']
    
    # Update the program
    update_data = {
        "name": "Updated Program Name",
        "description": "Updated description",
        "exercises": []
    }
    response = client.put(f'/programs/{program_id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == update_data['name']
    assert data['description'] == update_data['description']

def test_update_nonexistent_program(client):
    """Test updating a program that doesn't exist"""
    update_data = {
        "name": "Updated Program Name",
        "description": "Updated description",
        "exercises": []
    }
    response = client.put('/programs/nonexistent-id', json=update_data)
    assert response.status_code == 404 