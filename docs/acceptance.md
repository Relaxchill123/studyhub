Документ фиксирует приёмку ключевого сценария: изменения сохраняются между экземплярами PlannerService с одним и тем же path.

Автоматический smoke-тест

Файл: tests/test_persistent_planner.py
Запуск:python -m pytest tests/test_persistent_planner.py

Что проверяет:

1. Создать PlannerService с JsonStorage во временном path.
2. Добавить задачи Python и README.
3. Отметить Python выполненной.
4. Удалить README.
5. Создать новый PlannerService с тем же path.
6. Убедиться, что осталась ровно одна задача — выполненная Python.
7. Проверить статистику после нового экземпляра.

