from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data" / "tasks.txt"
DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_tasks():
    # if not DATA_FILE.exists():
        return []
    # return DATA_FILE.read_text(encoding="utf-8")

def save_tasks(text):
    # DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    # DATA_FILE.write_text(text, encoding="utf-8")
    ...

def load_titles(titles):
    if not titles:
        return []

    with DATA_FILE.open('r', encoding='UTF-8') as file:
        # print(file.read().split())
        # print(type(file.read().split()))
        for title in file.read().split('\n'):
            if title:
                titles.append(title)

        return titles

def save_titles(titles):
    with DATA_FILE.open('a', encoding='UTF-8') as file:
        for i in range(len(titles)):
            if i != len(titles) - 1:
                file.write(f"{titles[i]}\n")
            else:
                file.write(f"{titles[i]}")    