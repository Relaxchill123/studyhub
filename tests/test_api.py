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

def test_create_and_read_task(test_service):
    post_response = test_service.post(
            "/tasks",
            json={"title": "Изучить pytest", "priority": 3}
        )

    assert post_response.status_code == 201

    # post_response.json()["id"] == 3
    assert post_response.json()["title"] == "Изучить pytest"
    assert post_response.json()["priority"] == 3
    assert post_response.json()["is_done"] == False

    responce_task_id = post_response.json()["id"]

    response = test_service.get(f"/tasks/{responce_task_id}")

    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == responce_task_id
    assert data["title"] == "Изучить pytest"
    assert data["priority"] == 3
    assert data["is_done"] is False

def test_put_task(test_service):
    post_response = test_service.post(
            "/tasks",
            json={"title": "Изучить pytest", "priority": 3}
        )

    responce_task_id = post_response.json()["id"]
    
    response = test_service.put(
        f"/tasks/{responce_task_id}",
        json={"title": "Установить httpx2", "priority": 5, "is_done": True}
        )

    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == 1
    assert data["title"] == "Установить httpx2"
    assert data["priority"] == 5
    assert data["is_done"] is True

def test_patch_task(test_service):
    post_response = test_service.post(
                "/tasks",
                json={"title": "Изучить pytest", "priority": 3}
            )
    
    responce_task_id = post_response.json()["id"]
    
    response = test_service.patch(
        f"/tasks/{responce_task_id}",
        json={"priority": 5, "is_done": True}
        )

    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == 1
    assert data["title"] == "Изучить pytest"
    assert data["priority"] == 5
    assert data["is_done"] is True

    response = test_service.patch(
        f"/tasks/{responce_task_id}",
        json={"is_done": False}
        )

    data = response.json()

    assert data["is_done"] is False
    assert response.status_code == 200
    assert data["title"] == "Изучить pytest"
    assert data["priority"] == 5

def test_delete_task(test_service):
    post_response = test_service.post(
            "/tasks",
            json={"title": "Изучить pytest", "priority": 3}
        )

    responce_task_id = post_response.json()["id"]
    
    response = test_service.delete(f"/tasks/{responce_task_id}")

    assert response.status_code == 204
    
    assert response.content == b""

    response = test_service.delete(f"/tasks/{responce_task_id}")
    assert response.status_code == 404

    response = test_service.delete(f"/tasks/abc")
    assert response.status_code == 422

    response = test_service.get("/tasks")
    
    assert response.json() == []