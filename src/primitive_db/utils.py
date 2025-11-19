import json
import os

DATA_DIR = "data"

def load_table_data(table_name):
    """Загружает данные таблицы из JSON-файла."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_table_data(table_name, data):
    """Сохраняет данные таблицы в JSON-файл."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_metadata(filepath):
    """Загружает данные из JSON-файла."""
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({}, f, ensure_ascii=False, indent=2)
        return {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_metadata(filepath, data):
    """Сохраняет переданные данные в JSON-файл."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


