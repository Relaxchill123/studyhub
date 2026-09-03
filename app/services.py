from app.exceptions import TaskNotFoundError
from app.models import create_task
from app.validators import normalize_title

def get_titles(tasks):
    if not tasks:
        return []

    titles = []
    for task in tasks:
        if task.get('title'):
            titles.append(task['title'])

    return titles

def add_task(tasks, title, priority):
    ''' получает list, dict; возвращает str; изменяет tasks'''
    task_id = get_next_id(tasks)
    title = normalize_title(title)
    task = create_task(tasks, task_id, title, priority)
    
    tasks.append(task)
    
def get_next_id(tasks):
    ''' получает list; возвращает int; побочных эффектов не имеет'''
    if not tasks:
        return 1

    if len(tasks) == 1:
        return 2

    next_id = tasks[0]['id']
    for task in tasks:
        if task['id'] > next_id:
            next_id = task['id']
    return next_id + 1

def find_task(tasks, task_id):
    ''' получает list; возвращает dict/None; побочных эффектов не имеет '''
    for task in tasks:
        if task_id == task['id']:
            return task
    raise TaskNotFoundError(task_id)

def mark_done_tasks(tasks, task_id):
    ''' получает list; возвращает строку; изменяет tasks'''
    task = find_task(tasks, task_id)
    if not task['is_done']:
        task['is_done'] = True
        return "Отмечена как выполненная"
    return "Задача уже выполнена"

def get_stats(tasks):
    ''' получает list; возвращает строку; побочных эффектов не имеет'''
    done = 0
    not_done = 0
    for task in tasks:
        if task['is_done']:
            done += 1
        else:
            not_done +=1

    return (f"Задач выполнено: {done}; Задач не выполнено: {not_done}")