from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_encrypt_decrypt_success():
    # 1. Test Encrypt
    encrypt_response = client.post(
        "/api/encrypt",
        json={"message": "Mi secreto super seguro", "password": "mypassword123"}
    )
    assert encrypt_response.status_code == 200
    data = encrypt_response.json()
    assert "url_payload" in data
    
    payload = data["url_payload"]
    assert len(payload) > 0

    # 2. Test Decrypt with correct password
    decrypt_response = client.post(
        "/api/decrypt",
        json={"url_payload": payload, "password": "mypassword123"}
    )
    assert decrypt_response.status_code == 200
    decrypted_data = decrypt_response.json()
    assert "message" in decrypted_data
    assert decrypted_data["message"] == "Mi secreto super seguro"

def test_decrypt_wrong_password():
    # Encrypt a message
    encrypt_response = client.post(
        "/api/encrypt",
        json={"message": "Mensaje para fallar", "password": "correct_password"}
    )
    payload = encrypt_response.json()["url_payload"]

    # Try to decrypt with wrong password
    decrypt_response = client.post(
        "/api/decrypt",
        json={"url_payload": payload, "password": "wrong_password"}
    )
    assert decrypt_response.status_code == 400
    assert "detail" in decrypt_response.json()

def test_encrypt_empty_fields():
    # Missing password
    response1 = client.post(
        "/api/encrypt",
        json={"message": "Hello", "password": ""}
    )
    assert response1.status_code == 400
    
    # Missing message
    response2 = client.post(
        "/api/encrypt",
        json={"message": "", "password": "pass"}
    )
    assert response2.status_code == 400

def test_decrypt_invalid_payload():
    # Send garbage payload
    response = client.post(
        "/api/decrypt",
        json={"url_payload": "garbage_payload_that_is_not_base64", "password": "pass"}
    )
    assert response.status_code == 400
