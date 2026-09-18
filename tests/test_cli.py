from app.cli import add
from app.storage import MemoryStorage
from app.services import PlannerService

def test_add_command_smoke(monkeypatch):
    storage = MemoryStorage()
    service = PlannerService(storage)

    answers = iter(["Python", "4", "backend sql"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    result = add(service)

    assert result[1] == "Задача добавлена в tasks"
    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Python"
    assert tasks[0].priority == 4
    assert tasks[0].tags == ["backend", "sql"]