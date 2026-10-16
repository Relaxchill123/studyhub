import pytest

@pytest.mark.parametrize(
    ("title", "expected_status"),
    [("", 422), ("   ", 422), ("A", 201), ("A" * 120, 201),("A" * 121, 422), ("  "+"A" * 120+"  ", 201)],
)
def test_contract_title(test_service, title, expected_status):
    
    response = test_service.post(
        "/tasks",
        json={"title": title, "priority": 1},
    )
    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()["title"] == title.strip()
        assert set(response.json()) == {"id", "title", "priority", "is_done"}
        assert response.json()["is_done"] is False
    else:
        assert expected_status == 422
        assert response.json()["detail"][0]["loc"][-1] == "title"

@pytest.mark.parametrize(
    ("priority", "expected_status"),
    [(1, 201), (5, 201), (6, 422), (0, 422), ('high', 422)],
)
def test_contract_priority(test_service, priority, expected_status):
    response = test_service.post(
        "/tasks",
        json={"title": "test_task", "priority": priority},
    )
    assert response.status_code == expected_status
    if expected_status == 201:
        assert response.json()["priority"] == priority
        assert set(response.json()) == {"id", "title", "priority", "is_done"}
        assert response.json()["is_done"] is False
    else:
        assert expected_status == 422
        assert response.json()["detail"][0]["loc"][-1] == "priority"

@pytest.mark.parametrize(
    ("id", "expected_status"),
    [(1, 404), ('abc', 422)],
)
def test_get_contract_id(test_service, id, expected_status):
    response = test_service.get(
        f"/tasks/{id}",
    )
    assert response.status_code == expected_status

@pytest.mark.parametrize(
    ("id", "expected_status"),
    [(1, 404), ('abc', 422)],
)
def test_put_contract_id(test_service, id, expected_status):
    response = test_service.put(
            f"/tasks/{id}",
            json = {"title": "first_test_task", "priority": 3, "is_done": False}
        )
    assert response.status_code == expected_status

@pytest.mark.parametrize(
    ("id", "expected_status"),
    [(1, 404), ('abc', 422)],
)
def test_patch_contract_id(test_service, id, expected_status):
    response = test_service.patch(
            f"/tasks/{id}",
            json = {"title": "first_test_task"}
        )
    assert response.status_code == expected_status

@pytest.mark.parametrize(
    ("id", "expected_status"),
    [(1, 404), ('abc', 422)],
)
def test_delete_contract_id(test_service, id, expected_status):
    response = test_service.delete(
            f"/tasks/{id}",
        )
    assert response.status_code == expected_status

def test_contract_post(test_service):
    test_service.post("/tasks", json = {"title": "test_task", "priority": 4}).json()["id"]

    stats_before = test_service.get("/stats").json()
    tasks_before = test_service.get("/tasks").json()

    responce = test_service.post(f"/tasks", json={"title": "", "priority": 5})

    stats_after = test_service.get("/stats").json()
    tasks_after = test_service.get("/tasks").json()
    assert responce.status_code == 422
    assert stats_before == stats_after
    assert tasks_before == tasks_after

    responce = test_service.post(f"/tasks", json={"title": "test task", "priority": 0})
    
    stats_after = test_service.get("/stats").json()
    tasks_after = test_service.get("/tasks").json()
    assert responce.status_code == 422
    assert stats_before == stats_after
    assert tasks_before == tasks_after

def test_contract_put(test_service):
    task_id = test_service.post("/tasks", json = {"title": "test_task", "priority": 4}).json()["id"]

    stats_before = test_service.get("/stats").json()
    tasks_before = test_service.get(f"/tasks/{task_id}").json()

    responce = test_service.put(f"/tasks/{task_id}", json={"title": "test_task", "priority": 0, "is_done": True})

    stats_after = test_service.get("/stats").json()
    tasks_after = test_service.get(f"/tasks/{task_id}").json()
    assert responce.status_code == 422
    assert stats_before == stats_after
    assert tasks_before == tasks_after

    responce = test_service.put(f"/tasks/{task_id}", json={"title": "", "priority": 3, "is_done": True})
    
    stats_after = test_service.get("/stats").json()
    tasks_after = test_service.get(f"/tasks/{task_id}").json()
    assert responce.status_code == 422
    assert stats_before == stats_after
    assert tasks_before == tasks_after

    responce = test_service.put(f"/tasks/{task_id}", json={"title": "test_task", "priority": 4, "is_done": ""})
    
    stats_after = test_service.get("/stats").json()
    tasks_after = test_service.get(f"/tasks/{task_id}").json()
    assert responce.status_code == 422
    assert stats_before == stats_after
    assert tasks_before == tasks_after

    responce = test_service.put(f"/tasks/{task_id}", json={"priority": 4, "is_done": True})
    
    stats_after = test_service.get("/stats").json()
    tasks_after = test_service.get(f"/tasks/{task_id}").json()
    assert responce.status_code == 422
    assert stats_before == stats_after
    assert tasks_before == tasks_after

    responce = test_service.put(f"/tasks/{task_id}", json={"title": "complete_test_task", "priority": 5, "is_done": True})
    
    stats_after = test_service.get("/stats").json()
    tasks_after = test_service.get(f"/tasks/{task_id}").json()

    assert responce.status_code == 200
    assert stats_before['open'] == 1
    assert stats_before['done'] == 0

    assert stats_after['open'] == 0
    assert stats_after['done'] == 1

    assert tasks_before["title"] == "test_task"
    assert tasks_before["priority"] == 4
    assert tasks_before["is_done"] == False

    assert tasks_after["title"] == responce.json()["title"]
    assert tasks_after["priority"] == responce.json()["priority"]
    assert tasks_after["is_done"] == responce.json()["is_done"]

def test_contract_patch(test_service):
    task_id = test_service.post("/tasks", json = {"title": "test_task", "priority": 4}).json()["id"]

    stats_before = test_service.get("/stats").json()
    tasks_before = test_service.get(f"/tasks/{task_id}").json()

    responce = test_service.patch(f"/tasks/{task_id}", json={"title": ""})

    stats_after = test_service.get("/stats").json()
    tasks_after = test_service.get(f"/tasks/{task_id}").json()
    assert responce.status_code == 422
    assert stats_before == stats_after
    assert tasks_before == tasks_after

    responce = test_service.patch(f"/tasks/{task_id}", json={"is_done": True}).json()
    responce["is_done"] is True

    tasks_after = test_service.get(f"/tasks/{task_id}").json()
    assert tasks_after["id"] == responce["id"]
    assert tasks_after["title"] == responce["title"]
    assert tasks_after["priority"] == responce["priority"]
    assert tasks_after["is_done"] == responce["is_done"]

    responce = test_service.patch(f"/tasks/{task_id}", json={"is_done": False}).json()
    responce["is_done"] is False

    tasks_after = test_service.get(f"/tasks/{task_id}").json()
    assert tasks_after["id"] == responce["id"]
    assert tasks_after["title"] == responce["title"]
    assert tasks_after["priority"] == responce["priority"]
    assert tasks_after["is_done"] == responce["is_done"]

def test_tasks_filters_defaults(test_service):
    test_service.post("/tasks", json = {"title": "first_test_task", "priority": 4}).json()
    test_service.post("/tasks", json = {"title": "second_test_task", "priority": 3}).json()
    test_service.post("/tasks", json = {"title": "third_test_task", "priority": 5}).json()

    defaul_response = test_service.get(
        "/tasks",
        params={"sort_desc": False, "limit": 10},
    ).json()

    without_params_responce = test_service.get("/tasks").json()

    assert defaul_response == without_params_responce

@pytest.mark.parametrize(
    ("limit", "expected_status"),
    [(1, 200), (50, 200), (0, 422), (51, 422), ('abc', 422)],
)
def test_tasks_filters_limits(test_service, limit, expected_status):
    response = test_service.get(
        "/tasks",
        params={"sort_desc": False, "limit": limit},
    )

    assert response.status_code == expected_status

def test_unchaged_tasks_with_use_filters(test_service):
    first_task_id = test_service.post("/tasks", json = {"title": "first_test_task", "priority": 4}).json()["id"]
    second_task_id = test_service.post("/tasks", json = {"title": "second_test_task", "priority": 3}).json()["id"]
    third_task_id = test_service.post("/tasks", json = {"title": "third_test_task", "priority": 5}).json()["id"]

    test_service.patch(f"/tasks/{first_task_id}", json = {"is_done": True})
    test_service.patch(f"/tasks/{second_task_id}", json = {"is_done": True})

    stats_before = test_service.get("/stats").json()
    tasks_before = test_service.get("/tasks").json()

    response = test_service.get(
        f"/tasks",
        params={"is_done": False, "sort_desc": True, "limit": 1},
    )

    assert response.status_code == 200
    actual_ids = [t["id"] for t in response.json()]
    assert actual_ids == [third_task_id]

    stats_after = test_service.get("/stats").json()
    tasks_after = test_service.get("/tasks").json()

    assert stats_before == stats_after
    assert tasks_before == tasks_after

def test_open_schemas(test_service):
    document = test_service.get("/openapi.json").json()
    schemas = document["components"]["schemas"]
    assert set(schemas["TaskCreate"]["required"]) == {"title", "priority"}
    assert set(schemas["TaskUpdate"]["required"]) == {"title", "priority", "is_done"}
    assert set(schemas["TaskRead"]["required"]) == {"id", "title", "priority", "is_done"}
    assert schemas["TaskPatch"].get("required", []) == []
    assert "201" in document["paths"]["/tasks"]["post"]["responses"]