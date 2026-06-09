import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUTHOR = {
    "GIT_AUTHOR_NAME": "Зотов Владислав Сергеевич",
    "GIT_COMMITTER_NAME": "Зотов Владислав Сергеевич",
    "GIT_AUTHOR_EMAIL": "resolushhh@gmail.com",
    "GIT_COMMITTER_EMAIL": "resolushhh@gmail.com",
}


def run(*args, check=True):
    env = os.environ.copy()
    env.update(AUTHOR)
    result = subprocess.run(
        args,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=check,
    )
    return result.stdout.strip()


def commit(message, parent=None):
    run("git", "add", "-A")
    tree = run("git", "write-tree")
    if parent:
        commit_hash = run("git", "commit-tree", tree, "-p", parent, "-m", message)
    else:
        commit_hash = run("git", "commit-tree", tree, "-m", message)
    run("git", "update-ref", "refs/heads/main", commit_hash)
    run("git", "reset", "--hard", commit_hash)
    return commit_hash


def write(path, content):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(content, encoding="utf-8")


def remove(path):
    full = ROOT / path
    if full.exists():
        full.unlink()


def clean_extra():
    for path in [
        "src",
        "data",
        "tests",
        "assets",
        ".gitignore",
        "docs/report.md",
        "docs/history.md",
    ]:
        full = ROOT / path
        if full.is_dir():
            for item in sorted(full.rglob("*"), reverse=True):
                if item.is_file():
                    item.unlink()
            for item in sorted(full.rglob("*"), reverse=True):
                if item.is_dir():
                    item.rmdir()
            full.rmdir()
        elif full.is_file():
            full.unlink()


def main():
    clean_extra()

    write(
        "README.md",
        """# Student Task Journal

Учебный мини-проект для тренировки Git, GitHub и коммитов в VS Code.

Проект хранит список учебных задач и выводит его в консоль.

## Автор

ФИО: Зотов Владислав Сергеевич
Группа: РПО 9/1
""",
    )
    write(
        "docs/instruction.md",
        """# Инструкция пользователя

1. Откройте проект в VS Code.
2. Запустите файл src/main.py.
3. Посмотрите список задач из файла data/tasks.txt.
""",
    )
    c1 = commit("init: add project description")

    write(
        "src/main.py",
        """from helpers import load_tasks, print_tasks


def main():
    tasks = load_tasks("data/tasks.txt")
    print("=== Student Task Journal ===")
    print_tasks(tasks)


if __name__ == "__main__":
    main()
""",
    )
    write(
        "src/helpers.py",
        """def load_tasks(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            tasks = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return ["Файл data/tasks.txt пока не создан"]
    return tasks or ["Список задач пуст"]


def print_tasks(tasks):
    for number, task in enumerate(tasks, start=1):
        print(f"{number}. {task}")
""",
    )
    c2 = commit("feat: add task journal script", c1)

    write(
        "data/tasks.txt",
        """Подготовить README.md
Сделать первый коммит
Проверить историю в Git Graph
Опубликовать проект на GitHub
""",
    )
    c3 = commit("data: add sample tasks", c2)

    write(
        "docs/report.md",
        """# Отчёт по Git-практике

ФИО: Зотов Владислав Сергеевич
Группа: РПО 9/1
Ссылка на GitHub:

## Выполненные коммиты

1. init: add project description
2. feat: add task journal script
3. data: add sample tasks
4. docs: add report and test notes

## Что получилось

Создан учебный проект Student Task Journal с Python-скриптом, данными задач, документацией и настройкой Git-репозитория.
""",
    )
    write(
        "tests/smoke_test.md",
        """# Проверка запуска

Команда для проверки:

python src/main.py

Ожидаемый результат:

в консоли выводится список задач из data/tasks.txt.
""",
    )
    write(
        "assets/screenshots.txt",
        """Сюда впишите, какие скриншоты приложены к сдаче:

1. Source Control с изменениями.
2. GitHub-репозиторий.
3. Git Graph с историей коммитов.
""",
    )
    c4 = commit("docs: add report and test notes", c3)

    write(
        ".gitignore",
        """__pycache__/
*.pyc
.env
.vscode/
""",
    )
    c5 = commit("chore: add gitignore", c4)

    write(
        "README.md",
        """# Student Task Journal

Учебный мини-проект для тренировки Git, GitHub и коммитов в VS Code.

Проект хранит список учебных задач и выводит его в консоль.

## Автор

ФИО: Зотов Владислав Сергеевич
Группа: РПО 9/1

## Как запустить

1. Откройте терминал в корне проекта.
2. Выполните команду: python src/main.py
3. Проверьте, что в консоли появились задачи.
""",
    )
    write(
        "docs/report.md",
        """# Отчёт по Git-практике

ФИО: Зотов Владислав Сергеевич
Группа: РПО 9/1
Ссылка на GitHub:

## Выполненные коммиты

1. init: add project description
2. feat: add task journal script
3. data: add sample tasks
4. docs: add report and test notes
5. chore: add gitignore
6. docs: update usage information

## Что получилось

Создан учебный проект Student Task Journal с Python-скриптом, данными задач, документацией и настройкой Git-репозитория.
""",
    )
    c6 = commit("docs: update usage information", c5)

    remove("docs/instruction.md")
    write(
        "docs/history.md",
        """# История изменений проекта

- Создано описание проекта.
- Добавлены Python-файлы.
- Добавлены данные и отчёт.
- Настроен .gitignore.
- Старый файл инструкции заменён заметками об истории.
""",
    )
    c7 = commit("chore: replace instruction with history notes", c6)

    write(
        "docs/report.md",
        """# Отчёт по Git-практике

ФИО: Зотов Владислав Сергеевич
Группа: РПО 9/1
Ссылка на GitHub: https://github.com/Resolushh/practic_work

## Выполненные коммиты

1. init: add project description
2. feat: add task journal script
3. data: add sample tasks
4. docs: add report and test notes
5. chore: add gitignore
6. docs: update usage information
7. chore: replace instruction with history notes
8. docs: add github repository link

## Что получилось

Создан учебный проект Student Task Journal с Python-скриптом, данными задач, документацией и настройкой Git-репозитория.
""",
    )
    commit("docs: add github repository link", c7)

    print(run("git", "log", "--oneline"))


if __name__ == "__main__":
    main()
