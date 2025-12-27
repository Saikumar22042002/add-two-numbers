import pytest
from app import app as flask_app

@pytest.fixture(scope='module')
def client():
    """Create and configure a new app instance for each test module."""
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as test_client:
        yield test_client

def test_health_check(client):
    """Test the /health endpoint for a successful response."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_add_success(client):
    """Test the /add endpoint with valid integer inputs."""
    response = client.get('/add?a=5&b=10')
    assert response.status_code == 200
    assert response.json == {"inputs": {"a": 5.0, "b": 10.0}, "result": {"sum": 15.0}}

def test_add_with_floats(client):
    """Test the /add endpoint with valid float inputs."""
    response = client.get('/add?a=2.5&b=-1.5')
    assert response.status_code == 200
    assert response.json['result']['sum'] == 1.0

def test_add_missing_one_param(client):
    """Test the /add endpoint with one missing parameter."""
    response = client.get('/add?a=5')
    assert response.status_code == 400
    assert 'error' in response.json
    assert "Missing required query parameters" in response.json['error']

def test_add_missing_all_params(client):
    """Test the /add endpoint with no parameters."""
    response = client.get('/add')
    assert response.status_code == 400
    assert 'error' in response.json

def test_add_invalid_param_type(client):
    """Test the /add endpoint with a non-numeric parameter."""
    response = client.get('/add?a=five&b=10')
    assert response.status_code == 400
    assert 'error' in response.json
    assert "Invalid number format" in response.json['error']
