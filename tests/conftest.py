import pytest
import os
import tempfile
from app import app as flask_app
from exercise.database import init_db, get_db_connection

@pytest.fixture
def app():
    """Create a Flask app instance for testing"""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    flask_app.config['DATABASE'] = db_path
    flask_app.config['TESTING'] = True

    with flask_app.app_context():
        init_db()

    yield flask_app

    # Clean up
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Create a test client for the app"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test runner for the app"""
    return app.test_cli_runner()

@pytest.fixture
def sample_exercise():
    """Create a sample exercise for testing"""
    return {
        "type": "strength",
        "name": "Bench Press",
        "muscle_group": "chest",
        "info": "Standard bench press exercise"
    }

@pytest.fixture
def sample_program():
    """Create a sample program for testing"""
    return {
        "name": "Upper Body Workout",
        "description": "A comprehensive upper body workout",
        "exercises": []
    } 