from app.validators import normalize_title, is_normalized_priority, validate_command
from app.services import add_task, find_task, get_stats, mark_done_tasks
from app.exceptions import TaskNotFoundError

tasks = []
menu = ['Добавить задачу', 'Показать задачи', 'Найти задачу', 'Отметить выполненную задачу', 'Показать статистику', 'Выйти']

def run():
    while True:
        print()
        for i in range(0, len(menu)):
            print(f"{i+1}. {menu[i]}")
                
        command = input("\nВыбирете пункт меню: ")

        if validate_command(command):

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

                add_task(tasks,normalize_title(title), priority)

            if command == '6':
                print("Программа завершена")
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

                print(task, '\n')

            if command == '4':
                task_id = input('Введите ID задачи для изменения статуса: ')

                if not task_id:
                    print("\nID задачи не введен\n")
                    continue

                res = mark_done_tasks(tasks, int(task_id))

                if not res:
                    print("\nЗадачи с переданным ID нет в tasks\n")
                    continue

                print(res)            

            if command == '5':
                print(get_stats(tasks))
            
        else: 
            print("\nВыберите пункт меню корректно (число от 1 до 6)\n")

if __name__ == '__main__':
    run()