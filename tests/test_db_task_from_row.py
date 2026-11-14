import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from app.models import Task

from app.DBase.models import Base, TaskRow, task_from_row
from app.DBase.session import create_session_factory


@pytest.fixture
def isolated_database(tmp_path):
    database_file = tmp_path / "session.db"
    engine = create_engine(f"sqlite:///{database_file.as_posix()}")
    session_factory = create_session_factory(engine)
    Base.metadata.create_all(engine)
    try:
        yield engine, session_factory
    finally:
        engine.dispose()

def test_task_from_row(isolated_database):
    engine, session_factory = isolated_database

    first_task = TaskRow(
        title="Выполнить практику 68.1",
        priority=4,
        is_done=False,
        tags=['taskToToday'],
        title_normalized='выполнить практику 68.1'
    )

    second_task = TaskRow(
                title="Выполнить практику 68.2",
                priority=5,
                is_done=False,
                tags=[],
                title_normalized='выполнить практику 68.2'
            )

    with session_factory() as session:
        session.add(second_task)
        session.add(first_task)        
        session.flush()

        session.commit()

        print(session.get(TaskRow, 1))

        getted_task = select(TaskRow).order_by(TaskRow.id)
        task_rows = session.scalars(getted_task).all()

        returned_list = [task_from_row(task) for task in task_rows]

    returned_task = returned_list[0]

    planner_task = task_from_row(session.get(TaskRow, 1))

    assert isinstance(planner_task, Task)
    assert returned_task.id == planner_task.id
    assert returned_task.title == planner_task.title
    assert returned_task.priority == planner_task.priority
    assert returned_task.is_done == planner_task.is_done
    assert returned_task.tags == planner_task.tags
    assert session.get(TaskRow, 3) is None

    assert len(returned_list) == 2

    returned_list[0].tags.append('new_tag')

    assert returned_list[0].tags == ['new_tag']
    assert returned_list[1].tags == ['taskToToday']

    with pytest.raises(AttributeError):
        returned_list[1].title_normalized


    with session_factory() as session:
        getted_task = select(TaskRow).order_by(TaskRow.id)
        task_rows = session.scalars(getted_task).all()
        returned_list = [task_from_row(task) for task in task_rows]

        assert returned_list[0].tags == []
        assert returned_list[1].tags == ['taskToToday']