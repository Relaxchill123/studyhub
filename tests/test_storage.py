from app.models import Task
from app.storage import JsonStorage

def test_task_correct_save_to_json(tmp_path):
    path = tmp_path / 'tasks.json'
    storage = JsonStorage(path)

    tasks = [
        Task(1, "Python", 4),
        Task(2, "SQL", 1),
    ]

    storage.save(tasks)
    loaded = storage.load()

    assert loaded == tasks