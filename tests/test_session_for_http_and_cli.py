import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from tests.conftest import test_service
from app.DBase.models import Base, TaskRow
from app.DBase.session import create_session_factory

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api import app
from app.core.dependencies import get_db, get_planner
from app.main import build_service
from app.DBase.repositories import SqlTaskRepository
from app.services import PlannerService

def get_sql_planner(db: Session = Depends(get_db)) -> PlannerService:
    repository = SqlTaskRepository(db)
    return build_service(repository=repository)

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

def test_http_sqlrepo(isolated_database):
    engine, session_factory = isolated_database
    previous_factory = getattr(app.state, "session_factory", None)
    had_factory = hasattr(app.state, "session_factory")
    previous_overrides = app.dependency_overrides.copy()
    app.state.session_factory = session_factory
    try:
        app.dependency_overrides[get_planner] = get_sql_planner
        response = test_service.get("/tasks/7")
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)
        if had_factory:
            app.state.session_factory = previous_factory
        else:
            del app.state.session_factory
        task = TaskRow(
        title="Выполнить практику 68.1",
        priority=4,
        is_done=False,
        tags=['taskToToday'],
        title_normalized='выполнить практику 68.1'
    )

    with session_factory() as session:
        session.add(task)
        session.flush()
        task_id = task.id
        assert task_id is not None
        session.rollback()

    with session_factory() as session:
        assert session.get(TaskRow, task_id) is None

def test_correnct_and_uncorrect_task_in_transaction(isolated_database):
    task = TaskRow(
            title="Выполнить практику 68.1",
            priority=4,
            is_done=False,
            tags=['taskToToday'],
            title_normalized='выполнить практику 68.1'
        )

    uncorrect_task = TaskRow(
            title="Выполнить попытку внесения задачи с неекорректным priority",
            priority=0,
            is_done=False,
            tags=[],
            title_normalized="выполнить попытку внесения задачи с некорректным priority"
        )
    
    engine, session_factory = isolated_database

    with pytest.raises(IntegrityError):
        with session_factory() as session:
            session.add(task)   
            session.flush()
            session.add(uncorrect_task)
            try:
                session.flush()
            except IntegrityError:
                session.rollback()
                raise 

    with session_factory() as session:
        all_tasks = session.scalars(select(TaskRow)).all()
        assert all_tasks == []

def test_request_after_uncorrect_task(isolated_database):
    task = TaskRow(
            title="Выполнить практику 68.1",
            priority=4,
            is_done=False,
            tags=['taskToToday'],
            title_normalized='выполнить практику 68.1'
        )

    uncorrect_task = TaskRow(
            title="Выполнить попытку внесения задачи с неекорректным priority",
            priority=0,
            is_done=False,
            tags=[],
            title_normalized="выполнить попытку внесения задачи с некорректным priority"
        )
    
    engine, session_factory = isolated_database

    with session_factory() as session:
        with pytest.raises(IntegrityError):
            session.add(uncorrect_task)
            session.flush()

        with pytest.raises(PendingRollbackError):
            session.scalar(select(TaskRow.id))

        session.rollback()

        all_tasks = session.scalars(select(TaskRow)).all()
        assert all_tasks == []  

        session.add(task)
        session.flush()
        task_id = task.id
        session.commit()
        

    with session_factory() as session:
        saved_task = session.get(TaskRow, task_id)
        
        assert saved_task is not None
        assert saved_task.id == task_id
        assert saved_task.title == "Выполнить практику 68.1"
        assert saved_task.priority == 4
        assert saved_task.is_done is False
        assert saved_task.tags == ['taskToToday']
        assert saved_task.title_normalized == 'выполнить практику 68.1'

def test_clear_resourse(isolated_database):
    engine, session_factory = isolated_database

    task = TaskRow(
                title="Выполнить практику 68.1",
                priority=4,
                is_done=False,
                tags=['taskToToday'],
                title_normalized='выполнить практику 68.1'
            )

    uncorrect_task = TaskRow(
        title="Выполнить попытку внесения задачи с неекорректным priority",
        priority=0,
        is_done=False,
        tags=[],
        title_normalized="выполнить попытку внесения задачи с некорректным priority"
    )

    with pytest.raises(IntegrityError):
        with session_factory() as session:
            session.add(task)
            session.flush()

            session.add(uncorrect_task)
            session.flush()

        
    with session_factory() as session:
        all_tasks = session.scalars(select(TaskRow)).all()
        assert all_tasks == []