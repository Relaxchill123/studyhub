from app.storage import JsonStorage
from app.main import build_service
import pytest
from app.api import app
from fastapi.testclient import TestClient
from app.core.dependencies import get_planner

@pytest.fixture
def test_service(tmp_path):
    storage = JsonStorage(tmp_path / "tasks.json")
    planner = build_service(storage=storage)

    old_overrides = app.dependency_overrides.copy()

    app.dependency_overrides[get_planner] = get_test_planner

    def get_test_planner():
        return planner

    try:
        with TestClient(app, follow_redirects=False) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(old_overrides)