import json

class MemoryStorage: # для тестов, будет получать на вход список экземпляров класс Task
    def __init__(self, tasks: list = None):
        self._tasks = [] if tasks is None else tasks

    @property
    def tasks(self):
        return self._tasks

    @tasks.setter
    def tasks(self, task):
        self._tasks.append(task)

class JsonStorage:

    def __init__(self, data_file):
        self._data_file = data_file
        
    def load(self):

        if not self._data_file.exists():
            return []
        try:
            with self._data_file.open('r', encoding='utf-8') as file:
                value = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError(
                f"tasks.json повреждён: строка {error.lineno}"
            ) from error


        if not isinstance(value, list):
            raise ValueError("Ожидался список")

        return value
    
    def save(self, tasks):
        try:
            with self._data_file.open('w', encoding='utf-8') as file:
                json.dump(
                    tasks,
                    file,
                    ensure_ascii=False,
                    indent=2
                )
            return True
        except:
            return False

        

#     DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.json"
#     DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

#     def load_tasks():
#         if not DATA_FILE.exists():
#             return []
#         try:
#             with DATA_FILE.open('r', encoding='utf-8') as file:
#                 value = json.load(file)
#         except json.JSONDecodeError as error:
#             raise ValueError(
#                 f"tasks.json повреждён: строка {error.lineno}"
#             ) from error


#         if not isinstance(value, list):
#             raise ValueError("Ожидался список")

#         return value

#     def save_tasks(tasks):
#         DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
#         with DATA_FILE.open('w', encoding='utf-8') as file:
#             json.dump(
#                 tasks,
#                 file,
#                 ensure_ascii=False,
#                 indent=2
#             )

# def load_titles(titles):
#     if not titles:
#         return []

#     with DATA_FILE.open('r', encoding='UTF-8') as file:
#         # print(file.read().split())
#         # print(type(file.read().split()))
#         for title in file.read().split('\n'):
#             if title:
#                 titles.append(title)

#         return titles

# def save_titles(titles):
#     with DATA_FILE.open('a', encoding='UTF-8') as file:
#         for i in range(len(titles)):
#             if i != len(titles) - 1:
#                 file.write(f"{titles[i]}\n")
#             else:
#                 file.write(f"{titles[i]}")    