import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute(
    "CREATE TABLE checkins (id INTEGER PRIMARY KEY, title TEXT, priority INTEGER, is_done BOOLEAN)"
)
connection.execute(
    "INSERT INTO checkins (title, priority, is_done) VALUES (?, ?, ?)",
    ("Создать тестовое соединение", 2, 0))
connection.execute(
    "INSERT INTO checkins (title, priority, is_done) VALUES (?, ?, ?)",
    ("Отправить несколько INSERT-запросов", 3, 0))
connection.execute(
    "INSERT INTO checkins (title, priority, is_done) VALUES (?, ?, ?)",
    ("Проверить корректность выполнненых операций", 5, 0))

connection.commit()

# rows = connection.execute(
#     "SELECT id, title, priority, is_done FROM checkins WHERE id = ? ORDER BY priority DESC, id ASC LIMIT ?",
#     (0, 2),
# ).fetchall()

connection.execute(
    "UPDATE checkins SET priority = 4 WHERE id = 1"
)

rows = connection.execute(
    "SELECT * FROM checkins"
).fetchall()

connection.commit()

connection.execute(
    'UPDATE checkins SET priority = ? WHERE id = ?',
    (99, 1),
)

connection.rollback()

rows = connection.execute(
    "SELECT * FROM checkins WHERE id = 99"
).fetchall()

print(rows)
connection.close()