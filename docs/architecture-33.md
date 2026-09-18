PlannerService использует storage, но не является storage. Создайте коммит refactor: compose planner service with storage.

CLI → PlannerService → Task/Storage

## MemoryStorage и JsonStorage 

Используются для тестирования прогарммы (хранение в памяти программу) и для хранения в json-файле соответственно

MemoryStorage иcпользуется для тестирования, так как хранит данные в памяти программы и не сохраняет их после завершения, что и нужно при тестировании

JsonStorage используется для сохранения данных после завершения программы