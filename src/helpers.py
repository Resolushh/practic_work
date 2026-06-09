def load_tasks(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            tasks = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return ["Файл data/tasks.txt пока не создан"]
    return tasks or ["Список задач пуст"]


def print_tasks(tasks):
    for number, task in enumerate(tasks, start=1):
        print(f"{number}. {task}")
