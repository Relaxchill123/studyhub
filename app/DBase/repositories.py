from app.DBase.models import TaskRow, task_from_row
from app.models import Task

from sqlalchemy import select

class SqlTaskRepository():
    
    def list(self, session) -> list[Task]:
        statement = select(TaskRow).order_by(TaskRow.id)
        rows = session.scalars(statement).all()
        tasks = [task_from_row(row) for row in rows]
        return tasks

    def get(self, session, task_id) -> Task:
        row = session.get(TaskRow, task_id)
        if row is None:
            return None
        return task_from_row(row)