from app.storage import MemoryStorage
from app.services import PlannerService

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