from helpers import load_tasks, print_tasks


def main():
    tasks = load_tasks("data/tasks.txt")
    print("=== Student Task Journal ===")
    print_tasks(tasks)


if __name__ == "__main__":
    main()
