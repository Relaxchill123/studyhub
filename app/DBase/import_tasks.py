from pathlib import Path
import json
from sqlalchemy import select

from app.exceptions import StorageError
from app.core.config import load_settings
from app.models import Task
from app.DBase.models import TaskRow, Base
from app.DBase.engine import create_engine
from app.DBase.session import create_session_factory
from app.main import sql_service_context


def validate(task):
    if not isinstance(task['id'], int) and task['id'] <= 0:
        raise ValueError(
            f"ID {task['id']} должен быть числом положительным и больше 0"
        )

    if task['title'] != task['title'].strip() and not isinstance(task['title'], str):
        raise ValueError(
            f"У задачи c ID {task['title']} - некоректное название"
        )

    if not isinstance(task['is_done'], bool):
        raise ValueError(
            f"У задачи c ID {task['is_done']} - некоректное значение"
        )

    if task.get('tags') and not isinstance(task['tags'], list):
        raise ValueError(
            f"У задачи c ID {task['tags']} - поле tags не список"
        )

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

    if not tasks or not isinstance(tasks, list):
        raise StorageError("Корень JSON должен быть непустым списком")

    valid_tasks = []

    ids = []
    items = {'id', 'title', 'priority', 'is_done','tags'}

    for task in tasks:
        if set(task) - items:
            raise ValueError("В файле найдены недопустимые поля")            
        if validate(task):
            ids.append(task['id'])
            valid_tasks.append(task)

    if len(set(ids)) != len(ids):
        raise ValueError("ID не должны повторяться")


    try:
        valid_tasks = [Task.task_from_dict(task) for task in tasks]
    except KeyError as e:
        raise KeyError(f"Пропущено обязательное поле: {e}")


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
    Base.metadata.create_all(engine) # необходима, чтобы перенос выполнялся при вызове 
    # только этого файла
    session_factory = create_session_factory(engine)

    with session_factory() as session:

        tasks = session.scalars(select(TaskRow.id).limit(1)).first()

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

    return session.scalars(select(TaskRow)).all()

if __name__ == '__main__':
    settings = load_settings()
    put_to_sqlite(
        source=load_json_file(source=settings.json_path),
        target=settings.database_url
    )