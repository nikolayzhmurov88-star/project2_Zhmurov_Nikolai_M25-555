# src/primitive_db/utils.py

import json

def load_metadata(filepath):
    
    '''
    Загружает данные из JSON-файла.
    Если файл не найден, возвращает пустой словарь {}.
    '''

    try:
        with open(filepath, 'r') as f:
            return json.load(f)


    except FileNotFoundError:
        print("\nФайл не найден")
        return {}
    
    # except json.JSONDecodeError:
        # Обработка ошибки неправильного формата файла
        # return {}

def save_metadata(filepath, data):
    '''
    Сохраняет переданные данные в JSON-файл.
    '''
    with open(filepath, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


