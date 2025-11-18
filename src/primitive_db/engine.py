import shlex

import prompt

from .core import create_table, drop_table, list_tables
from .utils import load_metadata, save_metadata

METADATA_FILE = "db_meta.json"


def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """Главная функция с основным циклом программы"""
    print("***База данных***")
    print_help()

    metadata = load_metadata(METADATA_FILE)

    while True:
        metadata = load_metadata(METADATA_FILE)

        user_input = prompt.string('>>>Введите команду: ')

        args = shlex.split(user_input)

        if not args:
            continue

        command = args[0].lower()

        if command == "exit":
            print("Выход из программы...")
            break

        elif command == "help":
            print("***Процесс работы с таблицей***")
            print_help()

        elif command == "create_table":
            if len(args) < 3:
                print("Ошибка: Недостаточно аргументов.")
                continue

            table_name = args[1]
            columns = args[2:]

            result = create_table(metadata, table_name, columns)

            if result is not None:
                metadata = result
            save_metadata(METADATA_FILE, metadata)
 
        elif command == "drop_table":
            if len(args) != 2:
                print("Ошибка: Неверное количество аргументов.")
                continue

            table_name = args[1]
            result = drop_table(metadata, table_name)

            if result is not None:
                metadata = result
            save_metadata(METADATA_FILE, metadata)


        elif command == "list_tables":
            list_tables(metadata)

        else:
            print(f"Функции '{command}' нет. Попробуйте снова.")


if __name__ == "__main__":
    run()
