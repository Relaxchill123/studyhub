from app.models import Task
from app.storage import MemoryStorage
from app.services import PlannerService
import pytest

def test_task_clean_title():
    task = Task(1, '  hello   ', 4)

    assert task.title == 'hello'

def test_task_default_status():
    task = Task(1, '  hello   ', 4)

    assert task.is_done == False

def test_task_independent_tags():
    first_task = Task(1, '  hello   ', 4)
    second_task = Task(1, '  hello   ', 4)

    first_task.tags.append('f')

    assert not second_task.tags

def test_task_incorrect_priority():
    with pytest.raises(
        ValueError,
        match= '1 до 5'
    ):
        Task(
            1,
            'hello',
            0,
        )