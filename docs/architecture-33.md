PlannerService использует storage, но не является storage. Создайте коммит refactor: compose planner service with storage.

CLI → PlannerService → Task/Storage

## MemoryStorage и JsonStorage 

Используются для тестирования прогарммы (хранение в памяти программу) и для хранения в json-файле соответственно

На данный момент не реализована возможность редактирования json-файл (названия, приоритета задачи и т.д.)