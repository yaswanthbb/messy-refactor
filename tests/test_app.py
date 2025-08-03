import pytest
from app import create_app
from app.db import get_db_connection

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    # Setup: create clean test DB
    conn = get_db_connection()
    conn.execute("DELETE FROM users")
    conn.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", ("Test User", "test@example.com", "hashed"))
    conn.commit()
    conn.close()

    yield client

def test_health_check(client):
    res = client.get('/')
    assert res.status_code == 200

def test_get_users(client):
    res = client.get('/users')
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)

def test_create_user(client):
    res = client.post('/users', json={
        "name": "New User",
        "email": "new@example.com",
        "password": "securepass"
    })
    assert res.status_code == 201

def test_login_failure(client):
    res = client.post('/login', json={
        "email": "wrong@example.com",
        "password": "wrong"
    })
    assert res.status_code == 401

def test_missing_name_search(client):
    res = client.get('/search')
    assert res.status_code == 400
