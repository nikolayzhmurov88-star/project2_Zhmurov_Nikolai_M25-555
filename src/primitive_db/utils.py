# src/primitive_db/utils.py

import json
import os

def load_metadata(filepath):
    
    '''
    Загружает данные из JSON-файла.
    Если файл не найден, возвращает пустой словарь {}.
    '''
    
    full_path = 'src/primitive_db/data/' + filepath

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"\nФайл {filepath} не найден, создан новый")
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
		
        with open(full_path, 'w', encoding='utf-8') as f: 
            json.dump({}, f, ensure_ascii=False, indent=2)

    return {}
    

def save_metadata(filepath, data):
    '''
    Сохраняет переданные данные в JSON-файл.
    '''
    full_path = 'src/primitive_db/data/' + filepath
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_table_data(table_name):

    '''
    Загружает данные таблицы из JSON-файла.
    Если файл не найден, возвращает пустой список [].
    '''
    
    full_path = f'src/primitive_db/data/{table_name}.json'
   
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            return json.load(f)


    except FileNotFoundError:
        print(f"\nФайл таблицы {table_name} не найден, создан новый")
        
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

        return []

def save_table_data(table_name, data):

    '''
    Сохраняет переданные данные таблицы в JSON-файл.
    '''
    
    full_path = f'src/primitive_db/data/{table_name}.json' 
    
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    with open(full_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)