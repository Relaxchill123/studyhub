def test_task_http_path(test_service):
    main_post_response = test_service.post(
                    "/tasks",
                    json={"title": "Изучить pytest", "priority": 3}
                )

    off_post_response = test_service.post(
                    "/tasks",
                    json={"title": "Изучить GIT", "priority": 2}
                )

    task_id = main_post_response.json()["id"]

    stat_before = test_service.get("/stats")

    bad_put = test_service.put(
            f"/tasks/{task_id}",
            json={
                "title": "Изучить OOP",
                "is_done": True,
            }
        )

    bad_patch = test_service.patch(
        f"/tasks/{task_id}",
        json = {"priority": 'high'},
    )

    read_task = test_service.get(f"/tasks/{task_id}")

    stat_after = test_service.get("/stats")

    assert bad_put.status_code == 422    
    assert bad_patch.status_code == 422
    assert main_post_response.json() == read_task.json()
    assert stat_before.json() == stat_after.json()

    complete_put = test_service.put(
        f"/tasks/{task_id}",
        json={
            "title": "Изучить OOP",
            "priority": 5,
            "is_done": True,
        }
    )

    assert complete_put.status_code == 200
    assert complete_put.json()["id"] == task_id
    assert complete_put.json()["title"] == "Изучить OOP"
    assert complete_put.json()["priority"] == 5
    assert complete_put.json()["is_done"] == True

    read_task = test_service.get(f"/tasks/{task_id}")

    assert read_task.json() == complete_put.json()

    completed_patch = test_service.patch(
        f"/tasks/{task_id}",
        json = {"is_done": False}
    )

    read_task = test_service.get(f"/tasks/{task_id}")

    assert completed_patch.json()["is_done"] is False
    assert read_task.json()["is_done"] is False
    assert completed_patch.json() == read_task.json()

    deleted_task = test_service.delete(f"/tasks/{task_id}")

    assert deleted_task.status_code == 204

    second_delete_task = test_service.delete(f"/tasks/{task_id}")

    assert second_delete_task.status_code == 404

    read_tasks = test_service.get(f"/tasks").json()

    assert len(read_tasks) == 1
    assert read_tasks[0] == off_post_response.json()