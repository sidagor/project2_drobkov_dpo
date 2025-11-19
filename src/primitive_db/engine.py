import shlex

import prompt
from prettytable import PrettyTable

from .core import create_table, delete, drop_table, insert, list_tables, select, update
from .parser import parse_insert, parse_set_clause, parse_where_clause
from .utils import load_metadata, load_table_data, save_metadata, save_table_data

METADATA_FILE = "db_meta.json"


def print_help():
    """Выводит справочную информацию о командах для работы с таблицами и данными."""
    print("\n***Система управления базой данных***")    
    print("\nФункции для работы с таблицами:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> ... - "
          " создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nФункции для работы с данными:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) "
          "- создать запись")  
    print("<command> select from <имя_таблицы> where <столбец> = <значение> "
          "- прочитать записи по условию")  
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> "
          "where <столбец_условия> = <значение_условия> - обновить запись") 
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> "
          "- удалить запись")  
    print("<command> info <имя_таблицы> - вывести информацию о таблице")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")


def run():
    """Главная функция с основным циклом программы"""
    print("***База данных***")
    print_help()

    metadata = load_metadata(METADATA_FILE)
    data = {}

    while True:
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

        elif command == "insert" and args[1].lower() == "into":
            try:
               table_name, values = parse_insert(args)
            except Exception as e:
                print(f"Ошибка разбора команды: {e}")
                continue

            try:
                result = insert(metadata, table_name, values)
                if result is None:
                    continue
            except Exception as e:
                print(f"Ошибка при вставке: {e}")
  
        elif command == "select" and args[1].lower() == "from":
            table_name = args[2]
            table_data = load_table_data(table_name)
            if "where" in args:
                idx = args.index("where")
                try:
                    where_clause = parse_where_clause(args[idx + 1:idx + 4])
                except Exception as e:
                    print(e)
                    continue
            else:
                where_clause = None

            table_info = metadata.get(table_name)
            if not table_info:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            results = select(table_data, table_info, where_clause)
            if results:
                table_info = metadata[table_name]
                pt = PrettyTable()
                pt.field_names = [col for col, _ in table_info["columns"]]
                for row in results:
                    pt.add_row([row.get(col) for col, _ in table_info["columns"]])
                print(pt)
            else:
                print("Нет записей.")

        elif command == "update":
            table_name = args[1]
            if "set" not in args or "where" not in args:
                print("Ошибка: команда должна содержать 'set' и 'where'")
                continue
            set_idx = args.index("set")
            where_idx = args.index("where")
            try:
                set_clause = parse_set_clause(args[set_idx + 1:where_idx])
                where_clause = parse_where_clause(args[where_idx + 1:])
            except Exception as e:
                print(e)
                continue

            data = load_table_data(table_name)
            data = update(data, set_clause, where_clause)
            save_table_data(table_name, data)

        elif command == "delete" and args[1].lower() == "from":
            table_name = args[2]
            if "where" not in args:
                print("Ошибка: команда должна содержать 'where'")
                continue
            where_idx = args.index("where")
            try:
                where_clause = parse_where_clause(args[where_idx + 1:])
            except Exception as e:
                print(e)
                continue

            data = load_table_data(table_name)
            data = delete(data, where_clause)
            save_table_data(table_name, data)
         
        elif command == "info":
            table_name = args[1]
            table_info = metadata.get(table_name)
            if not table_info:
                print(f'Ошибка: Таблица "{table_name}" не существует.')
                continue
            table_data = load_table_data(table_name)
            cols = ", ".join([f"{col}:{typ}" for col, typ in table_info["columns"]])
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {cols}")
            print(f"Количество записей: {len(table_data)}")


        elif command == "list_tables":
            list_tables(metadata)

        else:
            print(f"Функции '{command}' нет. Попробуйте снова.")


if __name__ == "__main__":
    run()
