VALID_COMMANDS = {'1', '2', '3', '4', '5', '6'}
VALID_PRIORITYS = {'1', '2', '3', '4', '5'}
tasks = []

def show_menu():
    ''' ничего не получает; ничего не возвращает; побочных эффектов не имеет '''
    print("\n StudyHub Planner\n")
    print("1. Добавить задачу")
    print("2. Показать задачи")
    print("3. Найти задачу")
    print("4. Отметить выполненную задачу")
    print("5. Показать статистику")
    print("6. Выйти \n")

def valid_command(command):
    ''' получает str; возвращает bool; побочных эффектов не имеет '''
    cleaned = command.strip()
    return cleaned in VALID_COMMANDS

def add_task(tasks, title, priority=3):
    ''' получает list; ничего не возвращает; изменяет tasks'''
    id = get_next_id(tasks)

    tasks.append({
            'id': id,
            'title': title,
            'priority': priority,
            'is_done': False,
        })
    print(f"\nЗадача добавлена в tasks")

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

def normalize_title(title):
    ''' получает str; возвращает str; побочных эффектов не имеет '''
    return title.strip()

def is_normalized_priority(priority):
    ''' получает int; возвращет bool; побочных эффектов не имеет '''
    return 1 <= priority <=5

def show_tasks(tasks):
    ''' получает list; ничего не возвращает; побочных эффектов не имеет '''
    for task in tasks:
        print(f"ID: {task['id']}; Задача: {task['title']}; Приоритет: {task['priority']}; Статус: {task['is_done']}")

def find_task(tasks, task_id):
    ''' получает list; возвращает dict/None; побочных эффектов не имеет '''
    for task in tasks:
        if task_id == task['id']:
            return task
    return

def mark_done_tasks(tasks, task_id):
    ''' получает list; возвращает строку; изменяет tasks'''
    for task in tasks:
        if task_id == task['id']:
            if not task['is_done']:
                task['is_done'] = True
                return "Отмечена как выполненная"
            else:
                return "Задача уже выполнена"

    return None

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
        

while True:
    show_menu()
    command = input("\nВыбирете пункт меню: ")

    if valid_command(command):

        if command == '1':
            title = input("Введите задачу: ")

            if not title:
                print("\n Название не может быть пустым")
                continue

            priority = input("\n Введите приоритет: ")

            if not priority:
                priority = 3

            if not is_normalized_priority(int(priority)):
                print("\n Введите корректно приоритет задачи (число от 1 до 5)")
                continue

            add_task(tasks,normalize_title(title), priority)


        if not tasks:
            print("\n Спсиок задач - пуст")
            continue
        
        if command == '2':
            show_tasks(tasks)

        if command == '3':
            task_id = input('\nВведите ID задачи: ')

            if not task_id:
                print("ID не введен")
                continue

            task = find_task(tasks, int(task_id))
            
            if task:
                print(task)
            else:
                print("\nПереданной задачи нет в списке")

        if command == '4':
            task_id = input('Введите ID задачи для изменения статуса: ')

            if not task_id:
                print("ID задачи не введен")
                continue

            res = mark_done_tasks(tasks, int(task_id))

            if not res:
                print("\n Задачи с переданным ID нет в tasks")
                continue

            print(res)            

        if command == '5':
            print(get_stats(tasks))

        if command == '6':
            print("Программа завершена")
            break   
    else: 
        print("Выберите пункт меню корректно (число от 1 до 6)")