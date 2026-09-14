from app.exceptions import TaskNotFoundError
from app.models import Task

class PlannerService:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title, priority, tags = []): 
        ''' получает str, str, list; возвращает Task; изменяет tasks'''
        tasks = self.storage.load()

        if not tasks:
            next_id = 1
        
        elif len(tasks) == 1:
            next_id = 2

        else:
            next_id = tasks[0].id
            for task in tasks:
                if task.id > next_id:
                    next_id = task.id
            next_id = next_id + 1

        task = Task(next_id, title, priority, tags = tags)
        
        tasks.append(task)
        self.storage.save(tasks)
        return task
    

    def find_task(self, task_id, tasks=None):
        ''' получает list; возвращает dict/None; побочных эффектов не имеет '''
        if tasks is None:
            tasks = self.storage.load()

        for task in tasks:
            if task_id == task.id:
                return task
        raise TaskNotFoundError(task_id)

    def mark_done_tasks(self, task_id):
        ''' получает list; возвращает строку; изменяет tasks'''
        tasks = self.storage.load()
        task = self.find_task(task_id, tasks)

        if not task.is_done:
            task.mark_done()
            self.storage.save(tasks)
            return "Отмечена как выполненная"
        return "Задача уже выполнена"

    def get_stats(self):
        ''' получает list; возвращает строку; побочных эффектов не имеет'''
        tasks = self.storage.load()

        done = 0
        for task in tasks:
            if task.is_done:
                done += 1

        return (f"Задач всего: {len(tasks)}"
                f"Задач выполнено: {done}; Задач не выполнено: {len(tasks) - done}")

    def get_tasks(self):
        return self.storage.load()

    def remove_task(self, task_id):
        tasks = self.storage.load()
        task = self.find_task(task_id, tasks)
        tasks.remove(task) # pop удаляет задачу по переданному индексу, а нам нужно
        # удалять по полю id
        self.storage.save(tasks)
        return f"Задача: {task} - удалена"

    def add_tags(self, task_id, tags):
        tasks = self.storage.load()
        task = self.find_task(task_id, tasks)
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
            f"У задачи с ID: {task_id} тег(и) {', '.join(tags_in_task)} уже существуют"
        )