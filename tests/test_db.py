from sqlalchemy import URL, text
from app.DBase.engine import make_engine
from app.core.config import load_settings

import app.DBase.models
from app.DBase.models import TaskBase


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

    TaskBase.metadata.create_all(engine)

    with engine.connect() as connection:
        columns = connection.execute(text('PRAGMA table_info(tasks)')).all()
        create_sql = connection.execute(
            text('SELECT sql FROM sqlite_master WHERE type = :kind AND name = :name'),
            {'kind': 'table', 'name': 'tasks'},
        ).scalar_one()

    assert len(columns) == 6

    assert columns[0][5] == 1
    assert [not_null[3] for not_null in columns] == [1] * len(columns) - 1
    print("\n-------------\n", columns)
    print("\n-------------\n", create_sql)