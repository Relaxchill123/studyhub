from app.exceptions import TaskNotFoundError
from app.models import Task
from app.storage import JsonTaskRepository

class PlannerService:
    def __init__(self, storage):
        self.storage = storage
        self.jsonrepository = JsonTaskRepository(storage)

    def add_task(self, title, priority, tags=None):
        ''' получает str, str, list; возвращает Task; изменяет tasks'''
        tags = list(tags or [])
        tasks = self.storage.load()

        if not tasks:
            next_id = 1
        else:
            next_id = max([task.id for task in tasks]) + 1

        task = Task(next_id, title, priority, tags = tags)
        
        tasks.append(task)
        self.storage.save(tasks)
        return task
    

    def get_task(self, task_id: int) -> Task:
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError(
                "ID должен быть положительным числом"
            )

        task = self.jsonrepository.get(task_id)
        if task is None:
            raise TaskNotFoundError()
        return task

    def _find_task(self, task_id: int, tasks: list[Task]) -> Task:
        
        for task in tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError()

    def search_task(self, title):
        if not isinstance(title, str):
            return []
        return self.jsonrepository.search(title)

    def mark_done_tasks(self, task_id):
        ''' получает list; возвращает строку; изменяет tasks'''
        tasks = self.storage.load()
        task = self._find_task(task_id, tasks)

        if not task.is_done:
            task.mark_done()
            self.storage.save(tasks)
            return "Отмечена как выполненная"
        return "Задача уже выполнена"

    def get_stats(self):
        return self.jsonrepository.statics()

    def list_tasks(self):
        return self.jsonrepository.list()

    def remove_task(self, task_id):
        if task_id <= 0:
            raise ValueError
        tasks = self.storage.load()
        task = self._find_task(task_id, tasks)
        tasks.remove(task)
        self.storage.save(tasks)
        return f"Задача: {task} - удалена"

    def add_tags(self, task_id, tags):
        tasks = self.storage.load()
        task = self._find_task(task_id, tasks)
        tags_in_task = []

        for tag in tags:
            if tag not in task.tags: 
                task.add_tag_to_task(tag)
            else:
                tags_in_task.append(tag)

        self.storage.save(tasks)
        if not tags_in_task:
            return "Тег(и) успешно добавлены"

        new_tags = [tag for tag in tags if tag not in tags_in_task]
        
        return (
            f"Тег(и): {', '.join(new_tags)} добавлены;\n"
            f"У задачи с ID: {task_id} тег(и): {', '.join(tags_in_task)} уже существуют"
        )

    def select_tasks(self,
                    is_done: bool | None = None,
                    sort_desc=False,
                    limit=10
                ) -> list[Task]:
        
        return self.jsonrepository.select(
            is_done=is_done,
            sort_desc=sort_desc,
            limit=limit
        )

    def replace_task(self, task_id, title, priority, is_done):
        tasks = self.list_tasks()
        task = self._find_task(task_id, tasks)
        replace_task = Task(task.id, title, priority, is_done, task.tags)
        # "Сначала создай и проверь новую Task" - создание реализовал в строке
        # 114, не могу разобраться, что нужно проверить? Поля title, priority 
        # проверяются в models.py в __post_init__
        index_task_for_replace = tasks.index(task)
        tasks[index_task_for_replace] = replace_task
        self.storage.save(tasks)
        
        return replace_task

    def patch_task(self, task_id, title=None, priority=None, is_done=None):
        tasks = self.list_tasks()
        task = self._find_task(task_id, tasks)

        if title is None and priority is None and is_done is None:
            return task

        updated_task = Task(
            task.id,
            task.title if title is None else title,
            task.priority if priority is None else priority,
            task.is_done if is_done is None else is_done,
            task.tags.copy(),
        )

        index = tasks.index(task)
        tasks[index] = updated_task
        self.storage.save(tasks)
        return updated_task