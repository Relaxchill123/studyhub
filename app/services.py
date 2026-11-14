from app.exceptions import TaskNotFoundError
from app.models import Task
from app.storage import JsonTaskRepository

class PlannerService:
    def __init__(self, storage):
        self.storage = storage
        self.jsonrepository = JsonTaskRepository(storage)

    def add_task(self, title, priority, tags=None):
        tags = list(tags or [])
        
        task = self.jsonrepository.create(
            Task(id=0, title=title, priority=priority, tags = tags)
            )

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
        old_task = self.jsonrepository.get(task_id)
        if old_task is None:
            raise TaskNotFoundError()

        if old_task.is_done:
            return "Задача уже выполнена"

        return self.jsonrepository.mark_done(old_task.id)

    def get_stats(self):
        return self.jsonrepository.static()

    def list_tasks(self):
        return self.jsonrepository.list()

    def remove_task(self, task_id):
        if task_id <= 0:
            raise ValueError
        old_task = self.jsonrepository.get(task_id)
        if old_task is None:
            raise TaskNotFoundError()
        return self.jsonrepository.delete(old_task.id)

    def add_tags(self, task_id, tags):
        old_task = self.jsonrepository.get(task_id)
        if old_task is None:
            raise TaskNotFoundError()
        
        return self.jsonrepository.add_tags(old_task.id, tags)

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
        old_task = self.jsonrepository.get(task_id)
        if old_task is None:
            raise TaskNotFoundError()
        
        updated_task = Task(
            id=task_id,
            title=title,
            priority=priority,
            is_done=is_done,
            tags=old_task.tags
        )
        
        return self.jsonrepository.replace(task_id, updated_task)

    def patch_task(self, task_id, title=None, priority=None, is_done=None):
        old_task = self.jsonrepository.get(task_id)
        if old_task is None:
            raise TaskNotFoundError()

        if title is None and priority is None and is_done is None:
            return old_task

        updated_task = Task(
            old_task.id,
            old_task.title if title is None else title,
            old_task.priority if priority is None else priority,
            old_task.is_done if is_done is None else is_done,
            old_task.tags.copy(),
        )

        return self.jsonrepository.update(task_id, updated_task)