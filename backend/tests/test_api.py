from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_full_crud():
    # 1. CREATE (POST)
    create_response = client.post(
        "/api/messages",
        json={"message": "Mensaje original", "password": "mypassword123"}
    )
    assert create_response.status_code == 200
    msg_id = create_response.json()["id"]
    assert msg_id is not None

    # 2. UPDATE (PUT)
    update_response = client.put(
        f"/api/messages/{msg_id}",
        json={"message": "Mensaje actualizado", "password": "newpassword456"}
    )
    assert update_response.status_code == 200

    # 3. READ (GET)
    read_response = client.get(
        f"/api/messages/{msg_id}?password=newpassword456"
    )
    assert read_response.status_code == 200
    assert read_response.json()["message"] == "Mensaje actualizado"

    # Since the GET endpoint deletes the message after reading (read-once),
    # let's create a new one to test the explicit DELETE method.
    create_response2 = client.post(
        "/api/messages",
        json={"message": "Para borrar", "password": "pass"}
    )
    msg_id2 = create_response2.json()["id"]

    # 4. DELETE
    delete_response = client.delete(f"/api/messages/{msg_id2}")
    assert delete_response.status_code == 200

    # Verify it's deleted
    read_deleted = client.get(f"/api/messages/{msg_id2}?password=pass")
    assert read_deleted.status_code == 404
