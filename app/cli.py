from app.validators import validate_command

def show_menu():
    menu = ['Добавить задачу', 'Показать задачи', 'Найти задачу', 'Отметить выполненную задачу', 'Показать статистику', 'Выйти']

    print()
    for i in range(0, len(menu)):
        print(f"{i+1}. {menu[i]}")

def get_command():
    command = input("\nВыберите пункт меню: ").strip()
    if validate_command(command):
        return command

    print("\nВыберите пункт меню корректно (число от 1 до 6)\n")