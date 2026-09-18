import pytest
from app.storage import JsonStorage
from app.services import PlannerService
from app.exceptions import TaskNotFoundError, StorageError
from app.cli import add, find, remove, done, stats, get_command, show

def test_is_correct_user_path_in_persistent_planner(tmp_path, monkeypatch):
    path = tmp_path / 'data_path.json'
    storage = JsonStorage(path)
    service = PlannerService(storage)

    first_task = service.add_task('Python', 3)
    second_task = service.add_task('README', 3)

    service.mark_done_tasks(first_task.id)
    service.remove_task(second_task.id)

    new_service = PlannerService(JsonStorage(path))

    tasks = new_service.list_tasks()

    assert len(tasks) == 1
    assert tasks[0].title == "Python"
    assert tasks[0].is_done is True

    assert stats(new_service) == (
        "Задач всего: 1\n"
        "Задач выполнено: 1; Задач не выполнено: 0"
    )

    before = service.list_tasks()
    
    with pytest.raises(TaskNotFoundError):
        service.find_task(999)

    # assert service.list_tasks() == new_service.list_tasks()

    with pytest.raises(TaskNotFoundError):
        service.remove_task(999)

    # assert service.list_tasks() == new_service.list_tasks()

    with pytest.raises(TaskNotFoundError):
        service.mark_done_tasks(999)

    # assert service.list_tasks() == new_service.list_tasks()

    after = service.list_tasks()

    assert before == after

    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(StorageError):
        storage.load()
    
    with pytest.raises(StorageError):
        service.add_task('', 3)

    with pytest.raises(StorageError):
        service.add_task('Python', 6)

    path.write_text("{broken", encoding="utf-8")

    service = PlannerService(JsonStorage(path))

    with pytest.raises(StorageError):
        service.search_task("Python")

def test_cli_commands(tmp_path, monkeypatch, capsys):
    path = tmp_path / 'data_path'
    storage = JsonStorage(path)
    service = PlannerService(storage)

    answers = iter(['Python', '4', 'backend sql'])
    monkeypatch.setattr("builtins.input", lambda _:next(answers))

    result = add(service)

    show(service)
    captured = capsys.readouterr()
    assert "Python" in captured.out
    assert result[1] == 'Задача добавлена в tasks'
    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == 'Python'

    answers = iter(['1'])
    monkeypatch.setattr("builtins.input", lambda _:next(answers))

    result = done(service)
    tasks = service.list_tasks()

    assert result[1] == 'Отмечена как выполненная'
    assert tasks[0].is_done == True

    answers = iter(['1'])
    monkeypatch.setattr("builtins.input", lambda _:next(answers))

    result = find(service)

    assert result[1] == tasks[0]

    result = stats(service)

    assert result == "Задач всего: 1\nЗадач выполнено: 1; Задач не выполнено: 0"

    answers = iter(['1'])
    monkeypatch.setattr("builtins.input", lambda _:next(answers))

    result = remove(service)

    assert result[1] == f"Задача: {tasks[0]} - удалена"

    answers = iter(['999'])
    monkeypatch.setattr("builtins.input", lambda _:next(answers))

    result = get_command()

    assert result == "\nВыберите пункт меню корректно (число от 1 до 9)\n"

    answers = iter(['999'])
    monkeypatch.setattr("builtins.input", lambda _:next(answers))

    result = find(service)

    assert result[1] == "\nПереданной задачи нет в списке\n"



    # path.write_text("{broken", encoding="utf-8")
    # result = stats(service)

    # assert result == 'tasks.json повреждён: строка 1'