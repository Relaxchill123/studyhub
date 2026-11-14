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
        except (KeyError, ValueError, TypeError) as error:
            raise StorageError(
                "Некорректная запись задачи в JSON"
            ) from error
    
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


class JsonTaskRepository():
    def __init__(self, storage):
        self.storage = storage

    def list(self):
        return self.storage.load()

    def get(self, id: int) -> Task | None:
        tasks = self.storage.load()

        for task in tasks:
            if id == task.id:
                return task
        return None

    def select(self,
            is_done: bool | None = None,
            sort_desc=False,
            limit=10,
        ):

        tasks = self.storage.load()
        res_tasks = []

        if is_done is not None:
            res_tasks = list(
                filter(
                    lambda task: task.is_done == is_done, tasks
                    )
                )
        else:
            res_tasks = tasks.copy()

        return sorted(
            res_tasks,
            key=lambda x: x.id,reverse=sort_desc
        )[:limit]           

    def search(self, title: str):
        clean_title = title.strip().lower()

        if not clean_title:      
            return []

        tasks = self.storage.load()
        result = []        
        
        for task in tasks:
            if clean_title in task.title.lower():
                result.append(task)

        return result

    def statics(self):
        tasks = self.storage.load()
        done = 0

        for task in tasks:
            if task.is_done:
                done += 1

        return {
            'all': len(tasks),
            'open': len(tasks) - done,
            'done': done
        }

