import time
from functools import wraps


def log_time(func):
    
    '''
    Декоратор для замера времени выполнения функциии
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(f"\nФункция {func.__name__} выполнилась за {execution_time:.3f} секунд")
        return result
    return wrapper


def confirm_action(action_description):
    
    '''
    Декоратор для запроса подтверждения опасных операций
    '''
    
    def decorator(func):
        def wrapper(*args, **kwargs):

            # Запрос подтверждения у пользователя
            response = input(f'\nВы уверены, что хотите выполнить "{action_description}"? [y/n]: ').strip().lower()
            
            if response != 'y':
                print("\nОперация отменена.")
                return None
            
            # Если пользователь подтвердил, выполняем исходную функцию
            return func(*args, **kwargs)
        return wrapper
    return decorator


def create_cacher():

    '''
    Создает замыкание для кэширования результатов.
    '''

    # Кэш хранится в области видимости внешней функции
   
    cache = {}

    

    def cache_result(key, value_func):

        '''
        Внутренняя функция, которая кэширует результаты вызовов.
        '''

        # Проверяем, есть ли значение в кэше
        if key in cache:
            print(cache[key])
            return cache[key]
        
        # Если значения нет в кэше, вызываем функцию для получения данных
        result = value_func()  # Вызываем функцию для получения данных
        
        # Сохраняем результат в кэш
        cache[key] = result
        print(f'\nСохраняем в кэш ключ: {key}')

        return result

    def invalidate_cache(pattern=None):
        
        '''
        Очищает кэш полностью или по шаблону.
        '''
        if pattern is None:
            cache.clear()
            print('\nВесь кэш очищен')
        else:
            # Удаляем ключи, содержащие шаблон
            keys_to_remove = [k for k in cache.keys() if pattern in k]
            for key in keys_to_remove:
                del cache[key]
    
    cache_result.invalidate = invalidate_cache
    
    
        
    
    
    # Возвращаем внутреннюю функцию, которая запомнит переменную cache
    return cache_result


def handle_db_errors(func):
    
    '''
    Декоратор для обработки ошибок.
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
            
        except KeyError as e:
            print(f'\nОшибка: Таблица {e} не существует')
            return None
            
        except ValueError as e:
            print(e)
            if func.__name__ == 'parse_where_set_clause':
                return {}  # Для load_metadata он возращаем пустой словарь
            elif func.__name__ in 'parse_insert_values':
                return []  # Для load_metadata он возращаем пустой словарь
            else:
                return None  # Для остальных операций
            

        # Когда файл с информацией о базе данных или данными таблицы не найден     
        except FileNotFoundError:
            
            # Определяем что возвращать по имени функции
            if func.__name__ == 'load_metadata':
                return {}  # Для load_metadata он возращаем пустой словарь
            elif func.__name__ in 'load_table_data':
                return []  # Для load_metadata он возращаем пустой словарь
            else:
                return None  # Для остальных операций

        # Для других возможных ошибок   
        except Exception as e:
            print(f"Неожиданная ошибка в {func.__name__}: {e}")
            return None
    
    return wrapper