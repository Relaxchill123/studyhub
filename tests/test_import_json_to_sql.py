import json
import pytest
from sqlalchemy import create_engine, select

from app.exceptions import StorageError
from app.DBase.session import create_session_factory
from app.DBase.models import Base, TaskRow
from app.storage import JsonStorage
from app.models import Task
from app.DBase.import_tasks import load_json_file, put_to_sqlite
from app.services import PlannerService

@pytest.fixture
def isolated_database(tmp_path):
    database_file = tmp_path / "session.db"
    url = f"sqlite:///{database_file.as_posix()}"
    engine = create_engine(url)
    session_factory = create_session_factory(engine)
    Base.metadata.create_all(engine)
    try:
        yield engine, session_factory, url
    finally:
        engine.dispose()

def test_correct_import(tmp_path, isolated_database):
    engine, session_factory, url = isolated_database
    path = tmp_path / 'data_path'
    dict_tasks = [
        {
            "id": 1,
            "title": "gsdf",
            "priority": 2,
            "is_done": True,
            "tags": ['sql', 'py']
        },
        {
            "id": 2,
            "title": "wertte",
            "priority": 4,
            "is_done": False
        }
    ]

    path.write_text(json.dumps(dict_tasks, ensure_ascii=False), encoding="utf-8")

    tasks = put_to_sqlite(source=load_json_file(source=path), target=url)
    tasks_ids = [task.id for task in tasks]

    with session_factory() as session:
        ids_new_session = session.scalars(select(TaskRow.id)).all()
        assert tasks_ids == ids_new_session

        for i in range(len(tasks)):
            dict_tags = dict_tasks[i]['tags'] if dict_tasks[i].get('tags') else []
            assert tasks[i].title == dict_tasks[i]['title']
            assert tasks[i].priority == dict_tasks[i]['priority']
            assert tasks[i].is_done == dict_tasks[i]['is_done']
            assert tasks[i].tags == dict_tags

def test_bad_json_import(tmp_path, isolated_database):
    engine, session_factory, url = isolated_database
    path = tmp_path / 'data_path'
    storage = JsonStorage(path)
    service = PlannerService(storage)
    dict_tasks = [
            {
                "id": 1,
                "title": "gsdf",
                "priority": 2,
                "is_done": True,
                "tags": ['sql', 'py']
            },
            {
                "id": 2,
                "title": "wertte",
                "priority": 4,
                "is_done": True,
            }
        ]

    path.write_text(json.dumps(dict_tasks, ensure_ascii=False), encoding="utf-8")
    tasks = storage.load()
    storage.save(tasks)
    print("-----", service.list_tasks())

    with session_factory() as session:
        with pytest.raises(Exception):
            put_to_sqlite(source=load_json_file(source=path), target=url)  

        assert session.scalars(select(TaskRow)).all() == []

        service.add_task(title="123", priority=3)
        

def test_non_empty_target_import(tmp_path, isolated_database):
    engine, session_factory, url = isolated_database
    path = tmp_path / 'data_path'
    dict_tasks = [
        {
            "id": 1,
            "title": "gsdf",
            "priority": 2,
            "is_done": True,
            "tags": ['sql', 'py']
        },
        {
            "id": 2,
            "title": "wertte",
            "priority": 4,
            "is_done": False
        }
    ]

    path.write_text(json.dumps(dict_tasks, ensure_ascii=False), encoding="utf-8")
    
    with session_factory() as session:
        session.add(TaskRow(
                title="Выполнить практику 68.2",
                priority=5,
                is_done=False,
                tags=[],
                title_normalized='выполнить практику 68.2'
            ))

        task_id = session.scalars(select(TaskRow.id)).all()

        session.commit()

        with pytest.raises(ValueError):
            put_to_sqlite(source=load_json_file(source=path), target=url)

        assert session.scalars(select(TaskRow.id)).all() == task_id

def test_bad_path_source_import(tmp_path, isolated_database):
    engine, session_factory, url = isolated_database

    path = tmp_path / 'data_path'
    path.write_text(json.dumps([], ensure_ascii=False), encoding="utf-8")
    
    with pytest.raises(StorageError):
        put_to_sqlite(source=load_json_file(source=path), target=url)
