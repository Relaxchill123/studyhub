from pathlib import Path
from app.services import PlannerService
from app.exceptions import TaskNotFoundError, StorageError
from app.cli import show_menu, get_command, add, show, find, remove, done, stats, add_tags
from app.storage import JsonStorage, MemoryStorage

DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"

def run():

    storage = MemoryStorage() # DATA_FILE
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

        try:
            if not storage.load():
                print("\nСпсиок задач - пуст\n")
                continue
        except StorageError as e:
            print(e)
            break        

        if command == '2':
            show(services)

        if command == '3':
            res = find(services)
            if res:
                print(res)
            continue

        if command == '4':
            res = remove(services)
            if res:
                print(res)
            continue

        if command == '5':
            res = done(services)
            if res:
                print(res)
            continue

        if command == '6':
            print(stats(services))

        if command == '7':
            res = add_tags(services)
            if res:
                print(res)
            continue

if __name__ == '__main__':
    run()