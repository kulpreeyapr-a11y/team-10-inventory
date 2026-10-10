from fastapi.testclient import TestClient  # type: ignore
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_ask_question_success():
    response = client.post("/ask", json={"question": "ถอนวิชาได้ถึงสัปดาห์ไหน"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "source" in response.json()

def test_ask_question_empty():
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 400