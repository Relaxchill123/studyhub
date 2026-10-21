from app.storage import JsonStorage
from app.main import build_service
import pytest
from app.api import app
from fastapi.testclient import TestClient

@pytest.fixture
def test_service(tmp_path):
    storage = JsonStorage(tmp_path / "tasks.json")
    previous_service = app.state.planner
    app.state.planner = build_service(storage)
    try:
        with TestClient(app, follow_redirects=False) as client:
            yield client
    finally:
        app.state.planner = previous_service