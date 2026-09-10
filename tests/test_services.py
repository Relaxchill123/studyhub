from app.storage import MemoryStorage
from app.services import PlannerService

def test_add_task_returns_created_task():
    storage = MemoryStorage()
    service = PlannerService(storage)

    task = service.add_task(
        title="Python",
        priority=4,
    )

    assert task.id == 1 # должна ли функция add_task возвращать
    # добавленную задачу
    assert task.title == "Python"
    assert storage.load() == [task]