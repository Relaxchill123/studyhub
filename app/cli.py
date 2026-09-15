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
        print(f"ERROR: {e}")
        return False
    except ValueError as e:
        print(f"ERROR {e}")
        return False
    return ("Задача добавлена в tasks")

def show(services):
    for task in services.get_tasks():
        print(f"{task}\n")

def find(services):
    task_id = input('\nВведите ID задачи: ').strip()
    
    if not task_id:
        print("\nID не введен\n")
        return False

    try:
        task = services.find_task(int(task_id))
    except TaskNotFoundError:
        print("\nПереданной задачи нет в списке\n")
        return False
    except ValueError:
        print("\nОжидалось число")
        return False

    return (f"{task}\n")

def remove(services):
    task_id = input('Введите ID задачи для удаления: ').strip()
    if not task_id:
        print("\nID задачи не введен\n")
        return False

    try:
        res = services.remove_task(int(task_id)) 
    except TaskNotFoundError:
        print(f'Задачи с ID: {task_id} - нет в списке')
        return False
    except ValueError:
        print("\nОжидалось число")
        return False

    return res

def done(services):
    task_id = input('Введите ID задачи для изменения статуса: ').strip()
    
    if not task_id:
        print("\nID задачи не введен\n")
        return False
    try:
        res = services.mark_done_tasks(int(task_id))
    except TaskNotFoundError:
        print("\nПереданной задачи нет в списке\n")
        return False
    except ValueError:
        print("\nОжидалось число")
        return False

    if not res:
        print("\nЗадачи с переданным ID нет в tasks\n")
        return False

    return res

def stats(services):
    return (services.get_stats())

def add_tags(services):
    task_id = input('Введите ID задачи для добавления тег(ов): ').strip()
                
    if not task_id:
        print("\nID задачи не введен\n")
        return False

    tags = input("\nВведите теги через пробел: ").split()

    if not tags:
        print("\nТег(и) для добавления не введены\n")
        return False

    try:
        res = services.add_tags(int(task_id), tags)
    except TaskNotFoundError:
        print("\nПереданной задачи нет в списке\n")
        return False
    except ValueError:
        print("\nОжидалось число")
        return False

    return res