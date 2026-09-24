Основной ресурс - tasks, он является collection, содержащей задачи 

Минимальное представление Task: id, title, priority и is_done

Путь к JSON-файлу или Python-класс не являются частью внешнего ресурса

Клиент получает представление, а не прямую ссылку на объект сервера

## Collection и item

collection - path /tasks

item - path /tasks/{task_id}

Роль task_id - обозначение конкретной задачи

Два метода для collection: GET, DELETE
Три метода для item: GET, POST, PATCH

GET /health - техническая проверка сервиса *GET /health - техническая проверка*

GET /tasks - чтение коллекции
query: is_done?, limit?
200: Task

укажите path task_id ???
GET /tasks/{task_id} - чтение одног ресурса
200: tasks[task_id]

POST /tasks - создание новой Task
body: {title: 'Python', 'priority': 3}
201: Task

укажите path task_id ???
PUT /tasks/{task_id} - для полной замены задачи
body: {'title': 'Git', priority: 3, 'is_done': false}
200

PATCH /tasks/{task_id} - для частичной замены задачи
body: {'title': 'SQL'}
200

укажите path task_id ???
DELETE /tasks/{task_id} - для удаления задачи
204

DELETE /tasks/{999} - результат 404 (неизвестная Task)
status сообщает исход, а не способ хранения
path и method уже определены, но path/query/body будут описаны позже
декораторы, schemas и storage-реализация в этой карте отсутствуют намеренно

## Input locations

GET tasks/task_id/4 - path как обязательный выбор конкретного item

query: is_done?, limit? - query как настройку чтения collection

body: title, priority -  body как данные создания, полной или частичной замены

Разберите task_id, is_done, limit, title и priority ???

отсутствие optional query не является ошибкой

50.3.1:

GET /tasks
query: is_done?, limit?
200: list[Task]

POST /tasks
body: {'title': 'Python', 'priority': 4}
201: Task, task_id

PATCH /tasks/{task_id}
body: {'priority': 2}
200: Task

GET /tasks/{999} 
404

PUT /tasks/{task_id}
404

PATCH /tasks/{task_id}
404

DELETE /tasks/{task_id}
404

404 - отсутствие выбранного item

400 - некорректный request

детальная валидация 422 будет описана позже

path/query/body уже распределены

storage и внутренние Python-объекты не являются частью внешнего примера