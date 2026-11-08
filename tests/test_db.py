from sqlalchemy import URL, text
from app.DBase.engine import make_engine
from app.core.config import load_settings

import app.DBase.models
from app.DBase.models import Base


def test_engine_selects_one_on_temporary_file(tmp_path):
    database_path = tmp_path / "probe.sqlite3"
    url = URL.create(
        "sqlite",
        database=database_path.as_posix(),
    ).render_as_string(hide_password=False)
    engine = make_engine(url)

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar_one() == 1
    finally:
        engine.dispose()


def test_default_url_uses_project_root(tmp_path, monkeypatch):
    project_root = tmp_path / "project"
    other_cwd = tmp_path / "elsewhere"
    other_cwd.mkdir()

    first = load_settings(environ={}, project_root=project_root)
    monkeypatch.chdir(other_cwd)
    second = load_settings(environ={}, project_root=project_root)

    assert first.database_url == second.database_url

    
def test_comparison_table(tmp_path):
    database_path = tmp_path / "probe.sqlite3"
    url = URL.create(
        "sqlite",
        database=database_path.as_posix(),
    ).render_as_string(hide_password=False)
    engine = make_engine(url)

    Base.metadata.create_all(engine)

    with engine.connect() as connection:
        columns = connection.execute(text('PRAGMA table_info(tasks)')).all()
        create_sql = connection.execute(
            text('SELECT sql FROM sqlite_master WHERE type = :kind AND name = :name'),
            {'kind': 'table', 'name': 'tasks'},
        ).scalar_one()

    assert len(columns) == 6

    assert columns[0][5] == 1

    for column in columns:
        assert column[3] == 1

    assert "check_id_positive" in create_sql
    assert "check_priority_range" in create_sql

    assert columns[0][1] == 'id'
    assert columns[1][1] == 'title'
    assert columns[2][1] == 'priority'
    assert columns[3][1] == 'is_done'
    assert columns[4][1] == 'tags'
    assert columns[5][1] == 'title_normalized'

    Base.metadata.create_all(engine)

    print("\n-------------\n", columns)
    print("\n-------------\n", create_sql)