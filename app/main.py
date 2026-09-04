from app.validators import is_normalized_priority
from app.services import add_task, find_task, get_stats, mark_done_tasks, get_next_id, get_titles
from app.exceptions import TaskNotFoundError
from app.storage import load_tasks, save_tasks, load_titles, save_titles
from app.cli import show_menu, get_command  

def run():
    tasks = load_tasks()
    # titles = load_titles(get_titles(tasks))

    while True:
        show_menu()
                        
        command = get_command()

        if command == '1':
            title = input("Введите задачу: ")

            if not title:
                print("\nНазвание не может быть пустым\n")
                continue

            priority = input("\nВведите приоритет: ")

            if not priority:
                priority = 3

            if not is_normalized_priority(int(priority)):
                print("\n Введите корректно приоритет задачи (число от 1 до 5)\n")
                continue

            add_task(tasks, title, priority)
            print("Задача добавлена в tasks")

        if command == '6':
            print("Программа завершена")
            save_tasks(tasks)
            # save_titles(get_titles(tasks))
            break   

        if not tasks:
            print("\nСпсиок задач - пуст\n")
            continue
        
        if command == '2':
            for task in tasks:
                print(f"ID: {task['id']}; Задача: {task['title']}; Приоритет: {task['priority']}; Статус: {task['is_done']}")

            print()

        if command == '3':
            task_id = input('\nВведите ID задачи: ')

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

            print(task, '\n')

        if command == '4':
            task_id = input('Введите ID задачи для изменения статуса: ')

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