VALID_COMMANDS = {'1', '2', '3', '4', '5', '6'}
VALID_PRIORITYS = {'1', '2', '3', '4', '5'}
tasks = []

def show_menu():
    print()
    print("StudyHub Planner")
    print("1. Добавить задачу")
    print("2. Показать задачи")
    print("3. Найти задачу")
    print("4. Отметить выполненную задачу")
    print("5. Показать статистику")
    print("6. Выйти")
    print()

def valid_command(command):
    cleaned = command.strip()
    return cleaned in VALID_COMMANDS

def add_task(tasks):
    id = get_next_id(tasks)
    while True:
        title = input("Введите задачу: ")
        title = normalize_title(title)

        if not title:
            print("Название не может быть пустым")
            continue        

        priority = input("Введите приоритет: ")
        if is_normalized_priority(priority):
            break

        continue

    tasks.append({
            'id': id,
            'title': title,
            'priority': priority,
            'is_done': False,
        })
    print(f"Задача добавлена в tasks")

def get_next_id(tasks):

    if not tasks:
        return 1

    if len(tasks) == 1:
        return 2

    next_id = tasks[0]['id']

    for task in tasks:
        if task['id'] > next_id:
            next_id = task['id']

    return next_id + 1

def normalize_title(title):
    return title.strip()

def is_normalized_priority(priority):
    if not priority:
        print("Введите приоритет задачи (число от 1 до 5)")
        return False

    if not 1 <= int(priority) <=5:
        print("Введите корректно приоритет задачи (число от 1 до 5)")
        return False

    return True

def show_tasks(tasks):
    if not tasks:
        print()
        print("Спсиок задач еще пуст")
        print()

    for task in tasks:
        print(f"ID: {task['id']}; Задача: {task['title']}; Приоритет: {task['priority']}; Статус: {task['is_done']}")

def find_task(tasks):
    if tasks:
        while True:
            task_id = input('Введите ID задачи: ')
            if task_id:
                task_id = int(task_id)
                if task_id not in get_tasks_ids(tasks):
                    print("Переданной задачи нет в списке")
                for task in tasks:
                    if task_id == task['id']:
                        print(f"ID: {task['id']}; Задача: {task['title']}; Приоритет: {task['priority']}; Статус: {task['is_done']}")
            else:
                print("ID задачи не введен")
                continue
            break
    else:
        print("Список задач - пуст")

def get_tasks_ids(tasks):
    ids = []

    for task in tasks:
        ids.append(task['id'])

    return ids

def mark_done_tasks(tasks):

    if tasks:
        while True:
            task_id = input('Введите ID задачи для изменения статуса: ')
            if task_id:
                task_id = int(task_id)
                if task_id not in get_tasks_ids(tasks):
                    print("Переданной задачи нет в списке, просмотреть список задач? Y/N")
                    res = input()
                    if res == "Y":
                        show_tasks(tasks)
                        mark_done_tasks(tasks) 
            else:
                print("ID задачи не введен")
                continue
            break
    else:
        print("Список задач - пуст")

    for task in tasks:
        if task_id == task['id']:
            if not task['is_done']:
                task['is_done'] = True
                print('Отмечена как выполненная')
            else:
                print("Задача уже выполнена")

def get_stats(tasks):
    done = 0
    not_done = 0

    if tasks:
        for task in tasks:
            if task['is_done']:
                done += 1
            else:
                not_done +=1
        print(f"Задач выполнено: {done}; Задач не выполнено: {not_done}")
    else:
        print("Cписок задач - пуст")

while True:
    show_menu()
    command = input("Выбирете пункт меню: ")
    if valid_command(command):

        if command == '1':
            add_task(tasks)

        if command == '2':
            show_tasks(tasks)

        if command == '3':
            find_task(tasks)

        if command == '4':
            mark_done_tasks(tasks)

        if command == '5':
            get_stats(tasks)

        if command == '6':
            print("Программа завершена")
            break   
    else: 
        print("Выберите пункт меню корректно (число от 1 до 6)")