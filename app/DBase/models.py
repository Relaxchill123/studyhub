from sqlalchemy import Integer, String, Boolean, JSON, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.models import Task

class Base(DeclarativeBase):
    pass

class TaskRow(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    priority: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=2
    )
    is_done: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False
    )
    tags: Mapped[list[str]] = mapped_column(
        JSON, 
        nullable=False, 
        default=list
    )
    title_normalized : Mapped[str] = mapped_column(
        String, 
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
                "id > 0",
                name="check_id_positive"
            ),
        CheckConstraint(
                "priority >= 1 AND priority <= 5",
                name="check_priority_range"
            ),
    )

def task_from_row(task_row: TaskRow) -> Task:
    return Task(
        id=task_row.id,
        title=task_row.title,
        priority=task_row.priority,
        is_done=task_row.is_done,
        tags=list(task_row.tags),
    )