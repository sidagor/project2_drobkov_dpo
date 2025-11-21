# src/decorators.py
import time

_cacher_instance = None

def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. "
                  "Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def confirm_action(action_name):
    """Декоратор для подтверждения опасных операций"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            question = f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            response = input(question)
            if response.lower() != 'y':
                print("Операция отменена.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

def log_time(func):
    """Декоратор для замера времени выполнения функции"""
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(f"Функция выполнилась за {execution_time:.3f} секунд")
        return result
    return wrapper

def create_cacher():
    """Фабрика для создания замыкания с кэшем"""
    cache = {}
    
    def cache_result(key, value_func):
        """Внутренняя функция для кэширования результатов"""
        if key in cache:
            print(f"Используется кэшированный результат для ключа: {key}")
            return cache[key]
        
        result = value_func()
        cache[key] = result
        print(f"Результат закэширован для ключа: {key}")
        return result
    
    def clear_cache():
        """Очистка кэша"""
        cache.clear()
        print("Кэш очищен")
    
    cache_result.clear = clear_cache
    cache_result.get_cache_size = lambda: len(cache)
    
    return cache_result

_cacher_instance = create_cacher()

def get_cacher():
    """Получение глобального экземпляра кэшера"""
    return _cacher_instance
