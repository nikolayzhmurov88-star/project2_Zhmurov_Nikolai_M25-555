# src/primitive_db/utils.py

import json

def load_metadata(filepath):
    
    '''
    Загружает данные из JSON-файла.
    Если файл не найден, возвращает пустой словарь {}.
    '''

    try:
        with open('src/primitive_db/data/' + filepath, 'r') as f:
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
    with open('src/primitive_db/data/' + filepath, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_table_data(table_name):

    '''
    Загружает данные таблицы из JSON-файла.
    Если файл не найден, возвращает пустой словарь {}.
    '''
   
    try:
        with open('src/primitive_db/data/' + table_name, 'r') as f:
            return json.load(f)


    except FileNotFoundError:
        print("\nФайл не найден")
        return {}

def save_table_data(table_name, data):

    '''
    Сохраняет переданные данные таблицы в JSON-файл.
    '''
    with open('src/primitive_db/data/' + table_name, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)