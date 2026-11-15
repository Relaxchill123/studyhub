import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from app.models import Task

from app.DBase.models import Base, TaskRow, task_from_row
from app.DBase.session import create_session_factory
from app.DBase.repositories import SqlTaskRepository

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

def test_correct_tasks_getted_repo(isolated_database):
    engine, session_factory = isolated_database

    sqlrepo = SqlTaskRepository()

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

    third_task = TaskRow(
                    title="Выполнить практику 70",
                    priority=2,
                    is_done=False,
                    tags=[],
                    title_normalized='выполнить практику 70'
                )

    with session_factory() as session:
        clear_rows =  sqlrepo.list(session)

        session.add(second_task)
        session.add(first_task)        
        session.add(third_task)   
        session.flush()
        session.commit()

        getted_task = sqlrepo.get(session, first_task.id)
        uncorrect_id = sqlrepo.get(session, 4)

        task_rows = sqlrepo.list(session)

    assert clear_rows == []
    assert uncorrect_id == None

    assert isinstance(getted_task, Task)
    assert getted_task.id == first_task.id
    assert getted_task.title == first_task.title
    assert getted_task.priority == first_task.priority
    assert getted_task.is_done == first_task.is_done
    assert getted_task.tags == first_task.tags

    assert isinstance(task_rows, list)
    assert len(task_rows) == 3
    assert [task.id for task in task_rows] == [1, 2 , 3]
    assert task_rows[1].id == first_task.id
    assert task_rows[1].title == first_task.title
    assert task_rows[1].priority == first_task.priority
    assert task_rows[1].is_done == first_task.is_done
    assert task_rows[1].tags == first_task.tags

    with session_factory() as session:
        getted_task = sqlrepo.get(session, first_task.id)
        uncorrect_id = sqlrepo.get(session, 4)

        assert isinstance(getted_task, Task)
        assert getted_task.id == first_task.id
        assert getted_task.title == first_task.title
        assert getted_task.priority == first_task.priority
        assert getted_task.is_done == first_task.is_done
        assert getted_task.tags == first_task.tags
    
        assert isinstance(task_rows, list)
        assert len(task_rows) == 3
        assert [task.id for task in task_rows] == [1, 2 , 3]
        assert task_rows[1].id == first_task.id
        assert task_rows[1].title == first_task.title
        assert task_rows[1].priority == first_task.priority
        assert task_rows[1].is_done == first_task.is_done
        assert task_rows[1].tags == first_task.tags

        