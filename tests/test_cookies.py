from app.core.config import Settings
from app.core.dependencies import get_settings
from app.api import app
from pathlib import Path

def test_saved_client_cookie(test_service):
    first_responce_after_put = test_service.put(
        "/preferences", 
        json = {'view': 'detailed'}
    )

    assert first_responce_after_put.status_code == 200
    assert first_responce_after_put.json()['view'] == 'detailed'

    second_responce = test_service.get("/preferences")

    assert second_responce.status_code == 200
    assert second_responce.json()['view'] == 'detailed'

    bad_responce = test_service.put(
        "/preferences", 
        json = {'view': ''}
    )

    assert bad_responce.status_code == 422
    assert bad_responce.json()["detail"][0]["loc"][1] == 'view'

    responce_after_bad_put = test_service.get("/preferences")

    assert responce_after_bad_put.status_code == 200
    assert responce_after_bad_put.json()['view'] == 'detailed'

    deleted_responce = test_service.delete("/preferences")

    assert deleted_responce.status_code == 204
    assert deleted_responce.content == b""

    responce_after_delete = test_service.get("/preferences")

    assert responce_after_delete.json()['view'] == 'compact'

    new_responce = test_service.get("/preferences", cookies={"planner_view": "admin"})

    assert new_responce.status_code == 200
    assert new_responce.json()["view"] == "compact"

    put_new_responce = test_service.put(
        "/preferences",
        json={"view": "detailed"},
        headers = {"X-Client-Version": '1'},
    )

    assert put_new_responce.headers['X-Planner-Version'] == '1'
    assert put_new_responce.json()['client_version'] == '1'

def test_secure_cookie_flag(test_service):

    secure_settings = Settings(
        json_path=Path("dummy.json"),
        app_name="Test",
        cookie_secure=True,
        database_url="sqlite:///:memory:"
    )
    app.dependency_overrides[get_settings] = lambda: secure_settings

    try:
        resp = test_service.put("/preferences", json={"view": "detailed"})
        
        assert resp.status_code == 200
        print(resp.headers["set-cookie"])
        assert "Secure" in resp.headers["set-cookie"]
        
    finally:
        app.dependency_overrides[get_settings] = lambda: Settings(
            cookie_secure=False,
        )