def main():
    build_task("3")
    # try:
    #     build_task("3")
    # except ValueError as e:
    #     return "Приоритет должен быть целым числом"

def build_task(raw_priority):
    normalize_priority("3") == 3

def normalize_priority(raw_priority):
    int(raw_priority)

main()