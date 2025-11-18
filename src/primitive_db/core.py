SUPPORTED_TYPES = {"int", "str", "bool"}

def create_table(metadata, table_name, columns):
    """Cоздает новую таблицу в метаданных."""

    if table_name in metadata and metadata[table_name].get("columns"):
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    table_columns = [("ID", "int")]

    for col_def in columns:
        if ':' not in col_def:
            print(f'Некорректное значение: "{col_def}". Попробуйте снова.')
            return metadata

        name, col_type = col_def.split(':', 1)
        name = name.strip()
        col_type = col_type.strip().lower()

        if not name:
            print(f'Некорректное значение: "{col_def}". Попробуйте снова.')
            return metadata

        if col_type not in SUPPORTED_TYPES:
            print(f'Некорректное значение: "{col_def}". Попробуйте снова.')
            return metadata

        table_columns.append((name, col_type))

    metadata[table_name] = {
        "columns": table_columns,
        "data": [],
        "next_id": 1
    }


    columns_str = ", ".join([f"{name}:{typ}" for name, typ in table_columns])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {columns_str}')

    return metadata

def drop_table(metadata, table_name):
    """Проверяет существование таблицы и  удаляет таблицу из метаданных"""

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata

def list_tables(metadata):
    """Показывает список всех таблиц."""
    if not metadata:
        print("Нет созданных таблиц.")
        return

    for table_name in metadata.keys():
        print(f"- {table_name}")
