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