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
from app.main import sql_service_context


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


def test_get_task_via_sql(sql_database, test_service):
    engine, session_factory = sql_database

    post_response = test_service.post(
        "/tasks",
        json={"title": "Изучить pytest", "priority": 3}
    )

    task_id = post_response.json()["id"]

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
        assert data["priority"] == 3
        assert data["is_done"] == False
        assert "tags" not in data 
        
        response_404 = client.get("/tasks/999")
        assert response_404.status_code == 404
        
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)

    get_responce = test_service.get(
        f"/tasks/{task_id}",
    )

    data = post_response.json()

    assert get_responce.status_code == 200
    assert get_responce.json()["id"] == task_id
    assert get_responce.json()["title"] == data["title"]
    assert get_responce.json()["priority"] == data["priority"]
    assert get_responce.json()["is_done"] == data["is_done"]

class TrackingSession(Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.was_closed = False

    def close(self):
        self.was_closed = True
        super().close()


def test_session_closes_on_success_and_error(sql_database):
    engine, _ = sql_database
    
    with engine.connect() as conn:
        session = Session(conn)
        session.add(TaskRow(id=1, title="Существующая", priority=3, is_done=False, tags=[], title_normalized="существующая"))
        session.commit()
        session.close()

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
        
        response = client.get("/tasks/1") 
        assert response.status_code == 200
        
        assert len(created_sessions) == 1
        assert created_sessions[0].was_closed is True
        
        def broken_planner(db=Depends(get_db)):
            raise ValueError("Искусственная ошибка")
        
        app.dependency_overrides[get_planner] = broken_planner
        
        with pytest.raises(ValueError, match="Искусственная ошибка"):
            client.get("/tasks/1")
            
        assert len(created_sessions) == 2
        assert created_sessions[1].was_closed is True

    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(original_overrides)
        app.state.session_factory = previous_factory


def test_cli_context_closes_session(sql_database):
    engine, session_factory  = sql_database

    with session_factory() as session:
        session.add(TaskRow(id=1, title="CLI Task", priority=2, is_done=False, tags=[], title_normalized="cli task"))
        session.commit()
    
    TrackingFactory = sessionmaker(bind=engine, class_=TrackingSession)
    created_sessions = []
    
    def factory_wrapper():
        session = TrackingFactory()
        created_sessions.append(session)
        return session
    
    with sql_service_context(factory_wrapper) as planner:
        task = planner.get_task(1)
        assert task.title == "CLI Task"

        assert len(created_sessions) == 1
        assert created_sessions[0].was_closed is False
        
    assert created_sessions[0].was_closed is True 

    with pytest.raises(ValueError, match="Ошибка в CLI"):
        with sql_service_context(factory_wrapper) as planner:
            # Тоже читаем данные до выброса ошибки
            planner.get_task(1)
            raise ValueError("Ошибка в CLI")
            
    assert len(created_sessions) == 2
    assert created_sessions[1].was_closed is True