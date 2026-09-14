from pathlib import Path
from app.services import PlannerService
from app.exceptions import TaskNotFoundError, StorageError
from app.cli import show_menu, get_command, add, is_tasks
from app.storage import JsonStorage, MemoryStorage

DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"

def run():

    storage = JsonStorage(DATA_FILE) # 
    services = PlannerService(storage)

    while True:
        show_menu()
                        
        command = get_command()

        if command == '1':
            res = add(services)
            if res:
                print(res)

            continue

        if command == '8':
            break


        is_tasks(storage)
        
        if command == '2':
            for task in services.get_tasks():
                print(f"{task}\n")

        if command == '3':
            task_id = input('\nВведите ID задачи: ').strip()

            if not task_id:
                print("\nID не введен\n")
                continue

            try:
                task = services.find_task(int(task_id))
            except TaskNotFoundError:
                print("\nПереданной задачи нет в списке\n")
                continue
            except ValueError:
                print("\nОжидалось число")
                continue

            print(f"{task}\n")

        if command == '4':
            task_id = input('Введите ID задачи для удаления: ').strip()
            if not task_id:
                print("\nID задачи не введен\n")
                continue

            try:
                res = services.remove_task(int(task_id)) 
            except IndexError:
                print(f'Задачи с ID: {task_id} - нет в списке')
                continue
            except ValueError:
                print("\nОжидалось число")
                continue

            print(res)

        if command == '5':
            task_id = input('Введите ID задачи для изменения статуса: ').strip()

            if not task_id:
                print("\nID задачи не введен\n")
                continue
            try:
                res = services.mark_done_tasks(int(task_id))
            except TaskNotFoundError:
                print("\nПереданной задачи нет в списке\n")
                continue
            except ValueError:
                print("\nОжидалось число")
                continue

            if not res:
                print("\nЗадачи с переданным ID нет в tasks\n")
                continue

            print(res)            

        if command == '6':
            print(services.get_stats())

        if command == '7':
            task_id = input('Введите ID задачи для добавления тег(ов): ').strip()
            
            if not task_id:
                print("\nID задачи не введен\n")
                continue

            tags = input("\nВведите теги через пробел: ").split()

            if not tags:
                print("\nТег(и) для добавления не введены\n")
                continue

            try:
                res = services.add_tags(int(task_id), tags)
            except TaskNotFoundError:
                print("\nПереданной задачи нет в списке\n")
                continue
            except ValueError:
                print("\nОжидалось число")
                continue

            print(res)

if __name__ == '__main__':
    run()