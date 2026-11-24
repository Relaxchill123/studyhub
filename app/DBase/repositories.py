from app.DBase.models import TaskRow, task_from_row
from app.models import Task

from sqlalchemy import select

class SqlTaskRepository:
    def __init__(self, session):
        self.session = session

    def list(self) -> list[Task]:
        statement = select(TaskRow).order_by(TaskRow.id)
        rows = self.session.scalars(statement).all()
        return [task_from_row(row) for row in rows]

    def get(self, task_id) -> Task:
        row = self.session.get(TaskRow, task_id)
        if row is None:
            return None
        return task_from_row(row)

    def create(self, title, priority) -> Task:
        task = TaskRow(
            title=title.strip(), 
            priority=priority,
            is_done=False,
            tags=[],
            title_normalized=title.strip().lower(),
        )

        self.session.add(task)
        self.session.flush()

        return task_from_row(task)

    def replace(self, task) -> Task:
        old_task = self.session.get(TaskRow, task.id)
        if old_task is None:
            return None

        old_task.title = task.title.strip()
        old_task.priority = task.priority
        old_task.is_done = task.is_done
        old_task.title_normalized = task.title.strip().lower()

        self.session.flush(old_task)
        
        return task_from_row(old_task)