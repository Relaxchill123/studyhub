import json
from app.models import Task
from app.exceptions import StorageError

class MemoryStorage: # для тестов, будет получать на вход список экземпляров класс Task
    def __init__(self, tasks=None):
        self._tasks = list(tasks or [])

    def load(self):
        return list(self._tasks)

    def save(self, tasks):
        self._tasks = list(tasks)

class JsonStorage:

    def __init__(self, data_file):
        self._data_file = data_file
        
    def load(self) ->  list[Task]:

        if not self._data_file.exists():
            return []
        try:
            with self._data_file.open('r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise StorageError(
                f"tasks.json повреждён: строка {error.lineno}"
            ) from error


        if not isinstance(data, list):
            raise StorageError("Корень JSON должен быть списком")

        try:
            return [Task.task_from_dict(item) for item in data]
        except KeyError as error:
            raise StorageError(
                f"В файле json.txt, у задачи отсутствует обязательный ключ(и) - {' ,'.join([e for e in error.args])}"
            ) from error
        except (ValueError, TypeError) as error:
            raise StorageError(
                f"В файле json.txt, задача №{error.args[1]} передана с ошибкой: {error.args[0]}"
            )
    
    def save(self, tasks):
        data = [task.task_to_dict() for task in tasks]

        try:
            self._data_file.parent.mkdir(parents=True, exist_ok=True)
            with self._data_file.open('w', encoding='utf-8') as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=2
                )
            return True # Обработка
        except OSError as error:
            raise StorageError("Не удалось сохранить задачи") from error