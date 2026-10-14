def test_health(test_service):
    response = test_service.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_tasks(test_service):
    response = test_service.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []

def test_stats_tasks(test_service):
    response = test_service.get("/stats")
    assert response.status_code == 200
    assert response.json() == {'total': 0, 'open': 0, 'done': 0}

# def test_create_task(test_service):
#     response = test_service.post(
#         "/tasks",
#         json={"title": "Изучить pytest", "priority": 3}
#     )
#     assert response.status_code == 201
#     data = response.json()

#     assert data["id"] == 1
#     assert data["title"] == "Изучить pytest"
#     assert data["priority"] == 3
#     assert data["is_done"] is False


def test_create_and_read_task(test_service):
    test_service.post(
            "/tasks",
            json={"title": "Изучить pytest", "priority": 3}
        )
    response = test_service.get("/tasks/1")

    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == 1
    assert data["title"] == "Изучить pytest"
    assert data["priority"] == 3
    assert data["is_done"] is False

def test_put_task(test_service):
    test_service.post(
            "/tasks",
            json={"title": "Изучить pytest", "priority": 3}
        )
    
    response = test_service.put(
        "/tasks/1",
        json={"title": "Установить httpx2", "priority": 5, "is_done": True}
        )

    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == 1
    assert data["title"] == "Установить httpx2"
    assert data["priority"] == 5
    assert data["is_done"] is True

def test_patch_task(test_service):
    test_service.post(
            "/tasks",
            json={"title": "Изучить pytest", "priority": 3}
        )
    
    response = test_service.patch(
        "/tasks/1",
        json={"priority": 5, "is_done": True}
        )

    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == 1
    assert data["title"] == "Изучить pytest"
    assert data["priority"] == 5
    assert data["is_done"] is True

def test_delete_task(test_service):
    test_service.post(
            "/tasks",
            json={"title": "Изучить pytest", "priority": 3}
        )
    
    response = test_service.delete("/tasks/1")

    assert response.status_code == 204

    response = test_service.get("/tasks")
    
    assert response.json() == []