import pytest
from app.storage import JsonStorage
from app.services import PlannerService
from app.exceptions import TaskNotFoundError, StorageError

def test_is_correct_user_path_in_persistent_planner(tmp_path):
    path = tmp_path / 'data_path'
    storage = JsonStorage(path)
    service = PlannerService(storage)

    first_task = service.add_task('Python', 3)
    second_task = service.add_task('README', 3)

    service.mark_done_tasks(first_task.id)
    service.remove_task(second_task.id)

    new_service = PlannerService(storage)

    assert service.get_tasks() == new_service.get_tasks()

    third_task = new_service.add_task('Git', 2)

    assert service.get_stats() == service.get_stats()
    
    with pytest.raises(TaskNotFoundError):
        assert service.find_task(999) == TaskNotFoundError

    assert service.get_tasks() == new_service.get_tasks()

    with pytest.raises(TaskNotFoundError):
        assert service.remove_task(999) == TaskNotFoundError

    assert service.get_tasks() == new_service.get_tasks()

    with pytest.raises(TaskNotFoundError):
        assert service.mark_done_tasks(999) == TaskNotFoundError

    assert service.get_tasks() == new_service.get_tasks()

    path.write_text("{broken", encoding="utf-8")

    storage_before_storage_error = path.read_text(encoding="utf-8")

    with pytest.raises(StorageError):
            assert storage.load() == StorageError
            storage_after_storage_error = path.read_text(encoding="utf-8")

            assert storage_before_storage_error != storage_after_storage_error
            assert storage_after_storage_error != []

    
    with pytest.raises(StorageError):
         assert service.add_task('', 3) == ValueError
         assert service.add_task('Python', 6) == ValueError