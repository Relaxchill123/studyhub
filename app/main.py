from pathlib import Path
from app.validators import is_normalized_priority
from app.services import PlannerService
from app.exceptions import TaskNotFoundError
from app.cli import show_menu, get_command  
from app.storage import JsonStorage, MemoryStorage

DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"
# .parent.mkdir(parents=True, exist_ok=True)

def run():

    storage = JsonStorage(DATA_FILE) # 
    services = PlannerService(storage)
    # titles = load_titles(get_titles(tasks))

    while True:
        show_menu()
                        
        command = get_command()

        if command == '1':
            title = input("Введите задачу: ")

            # if not title:
            #     print("\nНазвание не может быть пустым\n")
            #     continue

            try:
                priority = int(input("\nВведите приоритет: ").strip())
            except ValueError:
                print('Ожидалось число')
                continue

            if not priority:
                priority = 3

            tags = input("\nВведите теги через пробел: ").split()

            # if not is_normalized_priority(priority):
            #     print("\n Введите корректно приоритет задачи (число от 1 до 5)\n")
            #     continue
            try:
                services.add_task(title, priority, tags)
            except ValueError as e:
                print(f"ERROR {e}")
                continue
            print("Задача добавлена в tasks")

        if command == '8':
            break

        try:
            if not storage.load():
                print("\nСпсиок задач - пуст\n")
                continue
        except ValueError as e:
            print(e)
            continue
        
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