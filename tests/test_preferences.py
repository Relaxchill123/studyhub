import pytest
from app.storage import JsonStorage
from app.models import Task
from app.services import PlannerService

@pytest.mark.parametrize(
    ("planner_version", "expected_status"),
    [("1", 200), ("A" * 65, 422)],
)

def test_contract_title(tmp_path, test_service, planner_version, expected_status):
    tasks_before_tests = test_service.get("/tasks")
    stats_before_tests = test_service.get("/stats")

    path = tmp_path / 'data_path'
    storage = JsonStorage(path)
    storage.save([
        Task(2, "Ознакомиться с Pydantic", 4, tags=[]),
        Task(7, "Ознакомиться с FastAPI", 4, tags=[]),
    ])

    service = PlannerService(storage)

    cli_tasks_before = service.list_tasks()
    cli_stats_before = service.get_stats()
    
    response_without_header = test_service.get("/preferences")

    assert response_without_header.status_code == 200
    assert response_without_header.json()['view'] == 'compact'
    assert response_without_header.json()['client_version'] == None
    assert response_without_header.headers['X-Planner-Version'] == '1'

    response_with_correct_header = test_service.get(
            "preferences",
            headers={"X-Client-Version": ''},
        )

    assert response_with_correct_header.status_code == 200
    assert response_with_correct_header.json()['client_version'] == ''
    assert response_with_correct_header.json()['view'] == 'compact'
    assert response_with_correct_header.headers['X-Planner-Version'] == '1'

    response = test_service.get(
        "/preferences",
        headers={"X-Client-Version": planner_version},
    )
    
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.headers['X-Planner-Version'] == '1'
        assert response.json()['view'] == 'compact'
        assert response.json()['client_version'] == '1'

    if expected_status == 422:
        print(response.json()["detail"])
        assert response.json()["detail"][0]["loc"][0] == 'header'

    tasks_after_tests = test_service.get("/tasks")
    stats_after_tests = test_service.get("/stats")

    cli_tasks_after = service.list_tasks()
    cli_stats_after = service.get_stats()

    assert cli_tasks_after == cli_tasks_before
    assert cli_stats_after == cli_stats_before
    assert tasks_before_tests.json() == tasks_after_tests.json()
    assert stats_before_tests.json() == stats_after_tests.json()