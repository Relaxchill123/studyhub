import pytest
from fastapi.testclient import TestClient
from app.api import app
from app.cli import find, done 
from app.services import PlannerService
from app.storage import JsonStorage

def test_api_and_cli_share_same_json(tmp_path, monkeypatch):
    path = tmp_path / "shared_tasks.json"
    storage = JsonStorage(path)
    service = PlannerService(storage)

    original_service = app.state.planner
    app.state.planner = service

    try:
        test_service = TestClient(app)

        post_response = test_service.post(
            "/tasks",
            json={"title": "Изучить pytest", "priority": 3}
        )
        assert post_response.status_code == 201
        task_id = post_response.json()["id"]
        
        assert post_response.json()["title"] == "Изучить pytest"
        assert post_response.json()["is_done"] is False

        answers = iter([str(task_id)])
        monkeypatch.setattr("builtins.input", lambda _: next(answers))
        
        result = find(service)
        
        assert result[0] is True
        assert result[1].id == task_id
        assert result[1].title == "Изучить pytest"

        answers = iter([str(task_id)])
        monkeypatch.setattr("builtins.input", lambda _: next(answers))
        
        result = done(service)
        assert result[1] == "Отмечена как выполненная" 

        response = test_service.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == task_id
        assert data["title"] == "Изучить pytest"
        assert data["is_done"] is True 

    finally:
        app.state.planner = original_service