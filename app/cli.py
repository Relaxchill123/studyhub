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

    return ("\nВыберите пункт меню корректно (число от 1 до 8)\n")

def add(services):
    title = input("Введите задачу: ")
    
    try:
        priority = int(input("\nВведите приоритет: ").strip())
    except ValueError:
        return (False, 'Ожидалось число')

    if not priority:
        priority = 3

    tags = input("\nВведите теги через пробел: ").split()

    try:
        services.add_task(title, priority, tags)
    except StorageError as e:
        return (False , e)
    except ValueError as e:
        return (False, e)
    return (True, "Задача добавлена в tasks")

def show(services):
    for task in services.list_tasks():
        print(f"{task}\n")

def find(services):
    task_id = input('\nВведите ID задачи: ').strip()
    
    if not task_id:
        return (False, '\nID не введен\n')

    try:
        task = services.find_task(int(task_id))
    except TaskNotFoundError:
        return (False, "\nПереданной задачи нет в списке\n")
    except ValueError:
        return (False, "\nОжидалось число")

    return (True, task)

def remove(services):
    task_id = input('Введите ID задачи для удаления: ').strip()
    if not task_id:
        return (False, "\nID задачи не введен\n")

    try:
        res = services.remove_task(int(task_id)) 
    except TaskNotFoundError:
        return (False, f'Задачи с ID: {task_id} - нет в списке')
    except ValueError:
        return (False, "\nОжидалось число")

    return (True, res)

def done(services):
    task_id = input('Введите ID задачи для изменения статуса: ').strip()
    
    if not task_id:
        return (False, "\nID задачи не введен\n")
    try:
        res = services.mark_done_tasks(int(task_id))
    except TaskNotFoundError:
        return (False,"\nПереданной задачи нет в списке\n")
    except ValueError:
        return (False, "\nОжидалось число")

    if not res:
        return (False, "\nЗадачи с переданным ID нет в tasks\n")

    return (True, res)

def stats(services):
    return services.get_stats()

def add_tags(services):
    task_id = input('Введите ID задачи для добавления тег(ов): ').strip()
                
    if not task_id:
        return (False, "\nID задачи не введен\n")

    tags = input("\nВведите теги через пробел: ").split()

    if not tags:
        return (False, "\nТег(и) для добавления не введены\n")

    try:
        res = services.add_tags(int(task_id), tags)
    except TaskNotFoundError:
        return (False, "\nПереданной задачи нет в списке\n")
    except ValueError:
        return (False, "\nОжидалось число")

    return (True, res)