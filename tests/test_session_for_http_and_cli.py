import pytest
from fastapi.testclient import TestClient
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from contextlib import contextmanager

from app.api import app
from app.core.dependencies import get_db, get_planner
from app.DBase.models import Base, TaskRow
from app.DBase.session import create_session_factory
from app.main import build_service
from app.DBase.repositories import SqlTaskRepository


@pytest.fixture
def sql_database(tmp_path):
    database_file = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{database_file.as_posix()}")
    Base.metadata.create_all(engine)
    session_factory = create_session_factory(engine)

    previous_factory = getattr(app.state, "session_factory", None)
    had_factory = hasattr(app.state, "session_factory")
    app.state.session_factory = session_factory
    
    yield engine, session_factory

    if had_factory:
        app.state.session_factory = previous_factory
    else:
        del app.state.session_factory
    engine.dispose()


def get_sql_planner(db=Depends(get_db)):
    repository = SqlTaskRepository(db)
    return build_service(repository=repository)



def test_get_task_via_sql(sql_database):
    engine, session_factory = sql_database

    with session_factory() as session:
        task_row = TaskRow(
            id=7, title="SQL Задача", priority=3, is_done=False, tags=["sql"], title_normalized="sql задача"
        )
        session.add(task_row)
        session.commit()

    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_planner] = get_sql_planner
    
    try:
        client = TestClient(app)
        response = client.get("/tasks/7")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 7
        assert data["title"] == "SQL Задача"
        assert "tags" not in data 
        
        response_404 = client.get("/tasks/999")
        assert response_404.status_code == 404
        
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)


class TrackingSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.was_closed = False

    def close(self):
        self.was_closed = True
        super().close()


def test_session_closes_on_success_and_error(sql_database):
    engine, _ = sql_database
    
    TrackingFactory = sessionmaker(bind=engine, class_=TrackingSession)
    created_sessions = []
    
    def factory_wrapper():
        session = TrackingFactory()
        created_sessions.append(session)
        return session

    previous_factory = getattr(app.state, "session_factory", None)
    app.state.session_factory = factory_wrapper
    
    original_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_planner] = get_sql_planner

    try:
        client = TestClient(app)
        
        client.get("/tasks/999")
        assert len(created_sessions) == 1
        assert created_sessions[0].was_closed is True
        
        def broken_planner(db=Depends(get_db)):
            raise ValueError("Искусственная ошибка")
        
        app.dependency_overrides[get_planner] = broken_planner
        
        with pytest.raises(ValueError, match="Искусственная ошибка"):
            client.get("/tasks/999")
            
        assert len(created_sessions) == 2
        assert created_sessions[1].was_closed is True

    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)
        app.state.session_factory = previous_factory


@contextmanager
def sql_service_context(session_factory):
    with session_factory() as db:
        yield build_service(repository=SqlTaskRepository(db))


def test_cli_sql_service_context(sql_database):
    engine, session_factory = sql_database
    
    with session_factory() as session:
        session.add(TaskRow(id=1, title="CLI Task", priority=2, is_done=False, tags=[], title_normalized="cli task"))
        session.commit()

    with sql_service_context(session_factory) as planner:
        task = planner.get_task(1)
        assert task.title == "CLI Task"
        
    with pytest.raises(ValueError, match="Ошибка в CLI"):
        with sql_service_context(session_factory) as planner:
            raise ValueError("Ошибка в CLI")