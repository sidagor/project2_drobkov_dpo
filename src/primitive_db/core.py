
from src.decorator import confirm_action, get_cacher, handle_db_errors, log_time

from .utils import load_table_data, save_table_data

SUPPORTED_TYPES = {"int", "str", "bool"}

@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Добавляет новую запись в таблицу"""
    table_info = metadata.get(table_name)
    if not table_info:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return None

    columns = table_info["columns"][1:]  
    if len(values) != len(columns):
        print("Ошибка: количество значений не соответствует количеству столбцов.")
        return None

    data = load_table_data(table_name)

    new_id = max([row["ID"] for row in data], default=0) + 1
    record = {"ID": new_id}

    for (col_name, col_type), value in zip(columns, values):
        if col_type == "int":
            value = int(value)
        elif col_type == "float":
            value = float(value)
        elif col_type == "bool":
            value = bool(value)
        elif col_type == "str":
            value = str(value)
        else:
            raise ValueError(f"Неизвестный тип {col_type}")
        
        record[col_name] = value

    data.append(record)
    save_table_data(table_name, data)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return data

@handle_db_errors
@log_time
def select(table_data, table_info, where_clause=None):
    """Возвращает записи таблицы, фильтруя по where_clause"""
    if not table_data:
        return []
    if not where_clause:
        return table_data

    cache_key = f"select_{id(table_info)}_{str(where_clause)}"
    cacher = get_cacher()

    def execute_select():
        filtered = []
        for row in table_data:
            if all(row.get(k) == v for k, v in where_clause.items()):
                filtered.append(row)
        return filtered
    
    return cacher(cache_key, execute_select)

@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет записи по условию"""
    updated_count = 0
    updated_ids = []
    for row in table_data:
        match = True
        for col, val in where_clause.items():
            if str(row.get(col)) != str(val):
                match = False
                break
        if match:
            for col, val in set_clause.items():
                row[col] = val
            updated_count += 1
            updated_ids.append(row.get('ID'))
    if updated_count == 0:
        print("Записи не найдены для обновления.")
    else:
        for record_id in updated_ids:
            print(f'Запись с ID={record_id} в таблице успешно обновлена.')
    
    return table_data
 
@handle_db_errors
@confirm_action("удаление записей") 
def delete(table_data, where_clause):
    """Удаляет записи по условию"""
    remaining = []
    deleted_count = 0
    deleted_ids = []
    for row in table_data:
        match = True
        for col, val in where_clause.items():
            if str(row.get(col)) != str(val):
                match = False
                break
        if match:
            deleted_count += 1
            deleted_ids.append(row.get('ID'))
        else:
            remaining.append(row)
    if deleted_count == 0:
        print("Записи не найдены для удаления.")
    else:
        for record_id in deleted_ids:
            print(f'Запись с ID={record_id} успешно удалена из таблицы')
    return remaining

@handle_db_errors
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

@confirm_action("удаление таблицы") 
@handle_db_errors
def drop_table(metadata, table_name):
    """Проверяет существование таблицы и  удаляет таблицу из метаданных"""

    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')

    return metadata

@handle_db_errors
def list_tables(metadata):
    """Показывает список всех таблиц."""
    if not metadata:
        print("Нет созданных таблиц.")
        return

    for table_name in metadata.keys():
        print(f"- {table_name}")

def clear_cache():
   """Очистка кэша запросов"""
   cacher = get_cacher()
   cacher.clear()       
