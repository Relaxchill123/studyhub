import pytest
from app.storage import MemoryStorage
from app.services import PlannerService
from app.models import Task

def test_repository_reads_fresh_data():
    storage = MemoryStorage()
    service = PlannerService(storage)

    created_task = service.add_task("Проверка свежести", priority=3)

    read_task = service.get_task(created_task.id)
    
    assert read_task.id == created_task.id
    assert read_task.title == "Проверка свежести"

    tasks = storage.load()
    tasks[0].title = "Изменено напрямую"
    storage.save(tasks)

    updated_task = service.get_task(created_task.id)
    
    assert updated_task.title == "Изменено напрямую"