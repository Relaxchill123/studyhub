from app.main import build_service
from app.storage import JsonStorage
from app.models import Task


def test_first_id_in_storage(tmp_path):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    service = build_service(storage)

    created = service.add_task("Задача с id 1", priority=3)

    assert created.id == 1
    assert created.is_done == False
    assert created.tags == []

def test_correct_id_in_non_empty_storage(tmp_path):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    service = build_service(storage)

    storage.save([
        Task(2, "Задача с id 2", 3, tags=[]),
        Task(7, "Задача с id 7", 5, tags=["work"]),
    ])

    created = service.add_task("Задача с id 8", priority=3)

    assert created.id == 8
    assert created.is_done == False
    assert created.tags == []

    reloaded = build_service(JsonStorage(path)).list_tasks()

    assert len(reloaded) == 3
    assert [t.id for t in reloaded] == [2, 7, 8]

def test_immutability_of_the_storage_after_reading_and_sorting(tmp_path):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    service = build_service(storage)

    storage.save([
            Task(2, "Задача с id 2", 3, tags=[]),
            Task(7, "Задача с id 7", 5, tags=["work"]),
            Task(9, "Задача с id 9", 2, tags=["Python"]),
            Task(1, "Задача с id 1", 1, tags=["GIT"]),
        ])

    service.mark_done_tasks(2)

    json_before = path.read_bytes()
    stat_before = service.get_stats()

    tasks = service.list_tasks()

    assert len(tasks) == 4

    task = service.find_task(2)

    assert task.id == 2
    assert task.title == 'Задача с id 2'
    assert task.priority == 3
    assert task.tags == []

    sorted_tasks = service.select_tasks(is_done=False, sort_desc=True, limit=2)

    assert len(sorted_tasks) == 2
    assert [task.id for task in sorted_tasks] == [9, 7]
    assert [task.is_done for task in sorted_tasks] == [False, False]

    json_after = path.read_bytes()
    stat_after = service.get_stats()

    assert json_before == json_after
    assert stat_before == stat_after

def test_correct_changes_replace_and_patch(tmp_path):
    path = tmp_path / "tasks.json"
    storage = JsonStorage(path)
    service = build_service(storage)

    storage.save([
            Task(2, "Задача с id 2", 2, tags=[]),
            Task(3, "Задача с id 3", 3, tags=["work"]),
        ])

    patched_task = service.patch_task(2, is_done=True)

    assert patched_task.is_done == True

    service_patched_task = service.patch_task(2, is_done=False)

    service_replaced_task = service.replace_task(3, "Задача по прежнему с id 3", 5, True)

    new_service = build_service(JsonStorage(path))

    new_service_patched_task = new_service.find_task(2)
    new_service_replaced_task = new_service.find_task(3)

    assert len(new_service.list_tasks()) == 2

    assert new_service_patched_task.id == 2
    assert new_service_patched_task.title == "Задача с id 2"
    assert new_service_patched_task.priority == 2
    assert new_service_patched_task.is_done is False
    assert new_service_patched_task.tags == []

    assert new_service_patched_task.id == service_patched_task.id
    assert new_service_patched_task.is_done == service_patched_task.is_done
    assert new_service_patched_task.tags == service_patched_task.tags

    assert new_service_replaced_task.id == service_replaced_task.id
    assert new_service_replaced_task.title == service_replaced_task.title
    assert new_service_replaced_task.priority == service_replaced_task.priority
    assert new_service_replaced_task.is_done == service_replaced_task.is_done