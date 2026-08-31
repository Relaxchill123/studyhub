back_28.py", line 2, in main
    build_task("high")
    ~~~~~~~~~~^^^^^^^^
  File "C:\Users\Администратор\Desktop\backend-course\studyhub\labs\traceback_28.py", line 5, in build_task
    normalize_prirotu(raw_priority)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "C:\Users\Администратор\Desktop\backend-course\studyhub\labs\traceback_28.py", line 8, in normalize_prirotu
    int(raw_priority)
    ~~~^^^^^^^^^^^^^^
ValueError: invalid literal for int() with base 10: 'high'

ValueError
invalid literal for int() with base 10: 'high'
int(raw_priority)
main -> build_task -> normalize_prirotu
raw_priority - строка

int("high")