from app.validators import validate_command
from app.exceptions import TaskNotFoundError, StorageError

def show_menu():
    menu = ['Добавить задачу', 'Показать задачи', 'Найти задачу',
            'Удалить задачу', 'Отметить выполненную задачу', 'Показать статистику',
            'Добавить тег(и)', 'Выйти']

    print()
    for i in range(0, len(menu)):
        print(f"{i+1}. {menu[i]}")

def get_command():
    command = input("\nВыберите пункт меню: ").strip()
    if validate_command(command):
        return command 

    print("\nВыберите пункт меню корректно (число от 1 до 8)\n")

def add(services):
    title = input("Введите задачу: ")
    
    try:
        priority = int(input("\nВведите приоритет: ").strip())
    except ValueError:
        print('Ожидалось число')
        return False

    if not priority:
        priority = 3

    tags = input("\nВведите теги через пробел: ").split()

    try:
        services.add_task(title, priority, tags)
    except StorageError as e:
        print(f"ERROR {e}")
        return False
    except ValueError as e:
        print(f"ERROR {e}")
        return False
    return ("Задача добавлена в tasks")

def is_tasks(storage):
    try:
        if not storage.load():
            print("\nСпсиок задач - пуст\n")
            return False
    except StorageError as e:
        print(e)
        return False

    return True