def create_task(tasks, id, title, priority=3):
    ''' получает list, str, int; возвращает dict; побочных эффектов не имеет'''
    return {
            'id': id,
            'title': title,
            'priority': priority,
            'is_done': False,
        }