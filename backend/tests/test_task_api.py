import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database.session import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use an in‑memory SQLite database for isolated testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_task():
    response = client.post("/tasks/", json={"title": "Test Task", "total_duration": 1800})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert "id" in data


def test_create_subtask():
    # Create a task first
    task_res = client.post("/tasks/", json={"title": "Task 1", "total_duration": 1800})
    task_id = task_res.json()["id"]

    response = client.post(f"/tasks/{task_id}/subtasks/", json={"title": "Sub 1", "duration": 900})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Sub 1"
    assert "id" in data
    assert data["task_id"] == task_id


def test_list_tasks():
    # Create two tasks
    t1_res = client.post("/tasks/", json={"title": "Task A", "total_duration": 1800}).json()
    t2_res = client.post("/tasks/", json={"title": "Task B", "total_duration": 2700}).json()

    resp = client.get("/tasks/")
    assert resp.status_code == 200
    tasks = resp.json()
    titles = {t["title"] for t in tasks}
    assert "Task A" in titles and "Task B" in titles


def test_get_task_detail():
    task_res = client.post("/tasks/", json={"title": "Detail Task", "total_duration": 1800}).json()
    task_id = task_res["id"]

    resp = client.get(f"/tasks/{task_id}/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == task_id
    assert data["title"] == "Detail Task"


def test_update_task():
    task_res = client.post("/tasks/", json={"title": "Update Me", "total_duration": 1800}).json()
    task_id = task_res["id"]

    resp = client.patch(f"/tasks/{task_id}/", json={"title": "Updated Title", "total_duration": 2400})
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Updated Title"
    assert data["total_duration"] == 2400


def test_delete_task():
    task_res = client.post("/tasks/", json={"title": "To Delete", "total_duration": 1800}).json()
    task_id = task_res["id"]

    resp = client.delete(f"/tasks/{task_id}/")
    assert resp.status_code == 200

    # Verify the task is gone
    resp = client.get(f"/tasks/{task_id}/")
    assert resp.status_code == 404

