from app.exceptions import StorageError 
import pytest
from app.storage import MemoryStorage, JsonStorage
from app.services import PlannerService
from app.models import Task

def test_add_task_returns_created_task():
    storage = MemoryStorage()
    service = PlannerService(storage)

    first_task = service.add_task(
        title="Python",
        priority=4,
    )

    second_task = service.add_task(
        title="SQL",
        priority=3
    )

    third_task = service.add_task(
        title="GIT",
        priority=3
    )

    assert third_task.id == 3
    assert first_task.is_done == False

    service.remove_task(second_task.id)
    service.mark_done_tasks(first_task.id)

    assert third_task.id == 3
    assert first_task.is_done == True

def test_new_id_task(tmp_path):
    path = tmp_path / 'data_path'
    storage = JsonStorage(path)
    storage.save([
        Task(2, "Ознакомиться с Pydantic", 4, tags=[]),
        Task(7, "Ознакомиться с FastAPI", 4, tags=[]),
    ])

    service = PlannerService(storage)

    new_task = service.add_task(
        title='GIT',
        priority=1,
    )

    assert new_task.id == 8

    new_storage = JsonStorage(path)
    new_service = PlannerService(new_storage)

    tasks = new_service.list_tasks()
    assert len(tasks) == 3

    by_id = {t.id: t for t in tasks}

    assert by_id[2].title == "Ознакомиться с Pydantic"
    assert by_id[2].priority == 4
    assert by_id[2].is_done is False
    assert by_id[2].tags == []

    assert by_id[7].title == "Ознакомиться с FastAPI"
    assert by_id[7].priority == 4
    assert by_id[7].is_done is False
    assert by_id[7].tags == []

    assert by_id[8].title == "GIT"
    assert by_id[8].priority == 1
    assert by_id[8].is_done is False
    assert by_id[8].tags == []

    def test_uncorrect_json_file(tmp_path, ra):
        path = tmp_path / 'data_path'
        path.write_text("{broken", encoding="utf-8")

        storage = JsonStorage(path)
        service = PlannerService(storage)

        with pytest.raises(StorageError):
            service.list_tasks()

        assert service.list_tasks() != []
        assert path.read_text(encoding="utf-8") == '{broken'