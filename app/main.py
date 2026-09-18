from pathlib import Path
from app.services import PlannerService
from app.exceptions import StorageError
from app.cli import show_menu, get_command, add, show, find, remove, done, stats, search, add_tags
from app.storage import JsonStorage, MemoryStorage

DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"

def run():

    storage = JsonStorage(DATA_FILE) # 
    services = PlannerService(storage)

    while True:
        show_menu()
                        
        command = get_command()

        try:
            services.list_tasks()
        except StorageError as e:
            print(e)
            break        

        if command == '1':
            res = add(services)
            if res[0]:
                print(res[1])
                continue
            print(res[1])
            continue

        if command == '9':
            break

        if not services.list_tasks():
            print("\nСпсиок задач - пуст\n")
            continue

        if command == '2':
            show(services)
            continue

        if command == '3':
            res = find(services)
            if res[0]:
                print(res[1])
                continue
            print(res[1])
            continue

        if command == '4':
            res = search(services)
            if not res[0]:
                print(res[1])
                continue
            continue

        if command == '5':
            res = remove(services)
            if res[0]:
                print(res[1])
                continue
            print(res[1])
            continue

        if command == '6':
            res = done(services)
            if res[0]:
                print(res[1])
                continue
            print(res[1])
            continue

        if command == '7':
            print(stats(services))
            continue

        if command == '8':
            res = add_tags(services)
            if res[0]:
                print(res[1])
                continue
            print(res[1])
            continue

        print(command)

if __name__ == '__main__':
    run()