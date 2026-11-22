from pathlib import Path
import json

from app.exceptions import StorageError
from app.core.config import load_settings
from app.models import Task
from app.DBase.models import TaskRow, Base
from app.DBase.engine import create_engine
from app.DBase.session import create_session_factory
from app.main import sql_service_context


def validate(task):
    if task.id <= 0:
        raise ValueError(f"ID {task.id} должен быть положительным и больше 0")

    if task.title != task.title.strip():
        raise ValueError(f"У задачи c ID {task.id} - некоректное название")

    return True

def load_json_file(source: Path):
    try:
        with source.open('r', encoding='utf-8') as file:
            tasks = json.load(file)
    except json.JSONDecodeError as error:
            raise StorageError(
                f"tasks.json повреждён: строка {error.lineno}"
            ) from error
    except FileNotFoundError:
        raise StorageError("По заданному пути файл не найден")
    except PermissionError:
        raise StorageError("К файлу по заданному пути нет доступа")

    if not isinstance(tasks, list):
        raise StorageError("Корень JSON должен быть списком")

    try:
        tasks = [Task.task_from_dict(task) for task in tasks]
    except KeyError as e:
        raise KeyError(f"Пропущено обязательное поле: {e}")

    valid_tasks = []

    ids = []
    for task in tasks:
      if validate(task):
        ids.append(task.id)
        valid_tasks.append(task)

    if len(set(ids)) != len(ids):
        raise ValueError("ID не должны повторяться")

    return [TaskRow(
            id=task.id,
            title=task.title,
            priority=task.priority,
            is_done=task.is_done,
            tags=task.tags,
            title_normalized=task.title.lower()
        ) for task in valid_tasks]

def put_to_sqlite(source: list[TaskRow], target):
    engine = create_engine(target)
    Base.metadata.create_all(engine)
    session_factory = create_session_factory(engine)

    with sql_service_context(session_factory) as planner:
        tasks = planner.list_tasks()

    with session_factory() as session:

        if tasks:
            raise ValueError("target должен быть пуст")

        try:
            for task in source:
                session.add(task)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    return tasks

settings = load_settings()
print(put_to_sqlite(
    source=load_json_file(source=settings.json_path),
    target=settings.database_url) 
) 