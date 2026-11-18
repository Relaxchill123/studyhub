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

    task = TaskRow(
        title="Выполнить практику 68.1",
        priority=4,
        is_done=False,
        tags=['taskToToday'],
        title_normalized='выполнить практику 68.1'
    )

    previous_factory = getattr(app.state, "session_factory", None)
    had_factory = hasattr(app.state, "session_factory")
    previous_overrides = app.dependency_overrides.copy()
    app.state.session_factory = session_factory
    try:
        app.dependency_overrides[get_planner] = get_sql_planner
        response = test_service.get("/tasks/1")
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous_overrides)
        if had_factory:
            app.state.session_factory = previous_factory
        else:
            del app.state.session_factory

