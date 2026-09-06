from pathlib import Path
from app.validators import is_normalized_priority
from app.services import add_task, find_task, get_stats, mark_done_tasks, get_next_id, get_titles, task_from_dict
from app.exceptions import TaskNotFoundError
# from app.storage import load_tasks, save_tasks, load_titles, save_titles
from app.cli import show_menu, get_command  
from app.storage import JsonStorage

DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"
# .parent.mkdir(parents=True, exist_ok=True)1

def run():
    tasks = []
    loaded_tasks = JsonStorage(DATA_FILE)
    for task in loaded_tasks.load():
        tasks.append(task_from_dict(task))
    # titles = load_titles(get_titles(tasks))

    while True:
        show_menu()
                        
        command = get_command()

        if command == '1':
            title = input("Введите задачу: ")

            # if not title:
            #     print("\nНазвание не может быть пустым\n")
            #     continue

            priority = input("\nВведите приоритет: ").strip()

            if not priority:
                priority = 3

            tags = input("\nВведите теги через пробел: ")

            if tags:
                tags = tags.split()
            else:
                tags = ''

            # if not is_normalized_priority(priority):
            #     print("\n Введите корректно приоритет задачи (число от 1 до 5)\n")
            #     continue
            try:
                add_task(tasks, title, priority, tags)
            except ValueError as e:
                print(f"ERROR {e}")
                continue
            print("Задача добавлена в tasks")

        if command == '6':
            tasks_for_save = []
            for task in tasks:
                tasks_for_save.append(task.task_to_dict())
            if not loaded_tasks.save(tasks_for_save):
                print("Сохранение данных не выполнено")
                break

            print("Программа завершена, данные сохранены корректно")
            # save_titles(get_titles(tasks))
            break   

        if not tasks:
            print("\nСпсиок задач - пуст\n")
            continue
        
        if command == '2':
            for task in tasks:
                print(f"{task}\n")

            print()

        if command == '3':
            task_id = input('\nВведите ID задачи: ').strip()

            if not task_id:
                print("\nID не введен\n")
                continue

            try:
                task = find_task(tasks, int(task_id))
            except TaskNotFoundError:
                print("\nПереданной задачи нет в списке\n")
                continue
            except ValueError:
                print("\nОжидалось число")
                continue

            print(f"{task}\n")

        if command == '4':
            task_id = input('Введите ID задачи для изменения статуса: ').strip()

            if not task_id:
                print("\nID задачи не введен\n")
                continue
            try:
                res = mark_done_tasks(tasks, int(task_id))
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

        if command == '5':
            print(get_stats(tasks))
        
if __name__ == '__main__':
    run()