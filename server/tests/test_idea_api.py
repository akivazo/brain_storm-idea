import pytest
import mongomock
import json
from ..idea_api import server, set_mongo_client
from uuid import uuid4
from flask.testing import FlaskClient

@pytest.fixture
def client():
    # Create a mock MongoDB client
    mock_mongo_client = mongomock.MongoClient()
    set_mongo_client(mock_mongo_client)
    
    # Set up Flask test client
    client = server.test_client()
    yield client
    mock_mongo_client.close()

def create_new_idea(client: FlaskClient, tags=["test"]):
    """
    Helper function to create a new idea through the API.
    """
    data = {
        "owner_name": "owner123",
        "subject": "Test Idea",
        "details": "Test idea details",
        "tags": tags
    }
    response = client.post("/idea", data=json.dumps(data), content_type="application/json")
    return response.get_json()["idea"]["id"]

def test_create_idea_success(client: FlaskClient):
    # Create valid idea data
    data = {
        "owner_name": "owner123",
        "subject": "New Idea",
        "details": "Details about the idea",
        "tags": ["tag1", "tag2"]
    }
    
    response = client.post("/idea", data=json.dumps(data), content_type="application/json")
    
    # Assert response status code and check for 'id' in response
    assert response.status_code == 201
    idea = response.get_json()["idea"]
    for key in data.keys():
        assert key in idea
    assert "id" in idea
    assert "time_created" in idea

def test_create_idea_invalid_data(client: FlaskClient):
    # Create invalid idea data (missing required fields)
    data = {
        "subject": "New Idea",
        "details": "Details about the idea"
    }
    
    response = client.post("/idea", data=json.dumps(data), content_type="application/json")
    
    # Assert response status code and error message for invalid data
    assert response.status_code == 400
    response_data = response.get_json()
    assert "error" in response_data

def test_get_idea_success(client: FlaskClient):
    idea_id = create_new_idea(client)
    
    # Retrieve the inserted idea using the API
    response = client.get(f"/idea/{idea_id}")
    
    # Assert response status code and check returned idea
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["idea"]["id"] == idea_id

def test_get_idea_not_found(client: FlaskClient):
    response = client.get(f"/idea/{uuid4()}")
    
    # Assert response status code for idea not found
    assert response.status_code == 404
    response_data = response.get_json()
    assert "was not found" in response_data

def test_get_all_ideas(client: FlaskClient):
    # Insert multiple ideas through the API
    create_new_idea(client, tags=["a", "b", "c"])  # Insert first idea
    create_new_idea(client, tags=["a", "b"])  # Insert second idea
    create_new_idea(client, tags=["a"])  # Insert second idea
    create_new_idea(client, tags=["d"])  # Insert second idea
    
    # Retrieve all ideas using the API
    response = client.get("/ideas")
    
    # Assert response status code and check returned ideas
    assert response.status_code == 200
    response_data = response.get_json()
    
    # Ensure all ideas were returned
    assert len(response_data["ideas"]) == 4

    # Retrieve all ideas with the specified tag using the API
    response = client.get("/ideas", query_string={"tag": ["a"]})
    
    # Assert response status code and check returned ideas
    assert response.status_code == 200
    response_data = response.get_json()
    
    # Ensure three ideas were returned
    assert len(response_data["ideas"]) == 3

    # Retrieve all ideas with the specified tag using the API
    response = client.get("/ideas", query_string={"tag": ["b", "c"]})
    
    # Assert response status code and check returned ideas
    assert response.status_code == 200
    response_data = response.get_json()
    
    # Ensure two ideas were returned
    assert len(response_data["ideas"]) == 2

def test_delete_idea(client: FlaskClient):
    # Insert a new idea through the API
    idea_id = create_new_idea(client)
    
    # Delete the inserted idea using the API
    response = client.delete(f"/idea/{idea_id}")
    
    # Assert response status code
    assert response.status_code == 204
    
    # Ensure idea no longer exists
    get_response = client.get(f"/idea/{idea_id}")
    assert get_response.status_code == 404

def test_favorite(client: FlaskClient):
    idea_id = create_new_idea(client)

    response = client.post(f"/favorite/{idea_id}")
    response = client.post(f"/favorite/{idea_id}")

    response = client.get(f"/idea/{idea_id}")

    assert response.status_code == 200

    idea = response.get_json()["idea"]

    assert idea["favorites"] == 2

    response = client.delete(f"/favorite/{idea_id}")

    response = client.get(f"/idea/{idea_id}")
    assert response.status_code == 200
    idea = response.get_json()["idea"]

    assert idea["favorites"] == 1

    response = client.delete(f"/favorite/{idea_id}")

    response = client.get(f"/idea/{idea_id}")
    assert response.status_code == 200
    idea = response.get_json()["idea"]

    assert idea["favorites"] == 0