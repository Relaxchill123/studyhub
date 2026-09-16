Риск | Уровень проверки | Сценарий | Ожидаемый результат

Пустой title | unit (Task) | Task(1, "   ", 3) | Название не может быть пустым
Приоритет не 1 - 5 | unit (Task) | Task(1, "Python", 6) | Приоритет должен быть от 1 до 5
Общий список tags у двух task | unit (Task) | task1 = Task(1, "Python", 2)
                                       task2 = Task(2, "Git", 2)
                                       task2.add_tags('programming')
                                       print(task1, task2) 
                                       # [ ] 1. Python 
                                       # [ ] 2. Git | Тэги: programming
MemoryStorage отдаёт внутренний список | unit (MemoryStorage) | load → изменить результат → load снова | Внутреннее состояние не изменилось
Потеря задач после перезапуска | integration (PlannerService + JsonStorage) | Новый service с тем же tmp_path | Задача видна после load
Повреждённый JSON | integration (JsonStorage) | Записать битый JSON, вызвать load | tasks.json повреждён: строка
Нет файла при первом запуске | integration (JsonStorage) | load() без файла | [], без исключения
Неизвестный id | integration (PlannerService) | mark_done(999) | TaskNotFoundError, состояние не изменилось, Переданной задачи нет в списке
CLI обходит сервис | smoke (CLI) | Прогнать add через диспетчер с подменённым input | JSON-логика не в CLI, задача в storage |
Пользовательский путь целиком | acceptance | add → done → remove → новый service → load | Состояние соответствует ожидаемому