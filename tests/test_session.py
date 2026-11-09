import pytest
from sqlalchemy import create_engine

from app.DBase.models import Base, TaskRow
from app.DBase.session import create_session_factory


@pytest.fixture
def session_factory(tmp_path):
    database_file = tmp_path / "session.db"
    engine = create_engine(f"sqlite:///{database_file.as_posix()}")
    Base.metadata.create_all(engine)
    try:
        yield create_session_factory(engine)
    finally:
        engine.dispose()


def test_taskrow_survives_an_independent_session(session_factory):
    row = TaskRow(
        title="Записать первую задачу",
        priority=2,
        is_done=False,
        tags=["session"],
        title_normalized="записать первую задачу",
    )

    with session_factory() as session:
        assert row.id is None
        session.add(row)
        assert row.id is None
        session.flush()
        task_id = row.id
        assert isinstance(task_id, int)

        session.commit()
        session.refresh(row)
        assert row.id == task_id
        assert row.title == "Записать первую задачу"
        assert row.priority == 2
        assert row.is_done is False
        assert row.tags == ["session"]
        assert row.title_normalized == "записать первую задачу"

    with session_factory() as session:
        saved = session.get(TaskRow, task_id)
        assert saved is not None
        assert saved.id == task_id
        assert saved.title == "Записать первую задачу"
        assert saved.priority == 2
        assert saved.is_done is False
        assert saved.tags == ["session"]
        assert saved.title_normalized == "записать первую задачу"


def test_default_tags_are_independent(session_factory):
    first = TaskRow(
        title="Первая заметка",
        priority=2,
        is_done=False,
        title_normalized="первая заметка",
    )
    second = TaskRow(
        title="Вторая заметка",
        priority=2,
        is_done=False,
        title_normalized="вторая заметка",
    )

    with session_factory() as session:
        session.add_all([first, second])
        session.flush()
        first_id = first.id
        second_id = second.id
        session.commit()

    with session_factory() as session:
        saved_first = session.get(TaskRow, first_id)
        saved_second = session.get(TaskRow, second_id)
        assert saved_first is not None
        assert saved_second is not None
        assert saved_first.tags == []
        assert saved_second.tags == []
        assert saved_first.tags is not saved_second.tags

        saved_first.tags.append("только в памяти первой строки")
        assert saved_second.tags == []