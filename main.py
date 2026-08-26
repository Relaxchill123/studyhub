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
    title = normalize_title(input("Введите задачу: "))
    while True:
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
    print(f"Задача {title} добавлена в tasks")
    print(tasks)

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
    cleaned = title.strip()
    if cleaned == "":
        print("Название не может быть пустым")
        add_task(tasks)
    return cleaned

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
            ...

        if command == '5':
            ...

        if command == '6':
            print("Программа завершена")
            break   
    else: 
        print("Выберите пункт меню корректно (число от 1 до 6)")