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