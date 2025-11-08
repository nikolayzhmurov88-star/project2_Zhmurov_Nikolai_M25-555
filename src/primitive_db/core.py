# src/primitive_db/core.py

def create_table(metadata, table_name, columns):
    
    '''
    Создаёт таблицу в метаданных.
    Добавляет столбец ID:int в начало списка столбцов.
    Проверяет существование таблицы и валидность типов.
    Возвращает обновлённый metadata или выводит ошибку.
    '''

    # Проверяем есть ли ключ 'table_name' в словаре 'metadata'
    if table_name in metadata:
        print(f"\nОшибка: Таблица '{table_name}' уже существует.")
        return

    # Создаем словарь с допустимыми типами данных
    valid_types = {'int', 'str', 'bool'}

    # Добавляем ID первым столцом в таблицу если этого не сделал пользователь
    if columns[0] == ('ID', 'int'):
        columns_with_id = columns
    else:
        columns_with_id = [('ID', 'int')] + columns
    
    # Проверяем допустимые ли типы данных у столбцов создаваемой таблицы
    for col_name, col_type in columns_with_id:
        if col_type not in valid_types:
            print(f"\nНеверный тип данных столбца '{col_type}' для столбца '{col_name}'. Допустимы: {valid_types}")
            return

    # Успешно создаем таблицу
    metadata[table_name] = columns_with_id
    
    # Формируем строку вывода объединяя элементы списка в строку 
    columns_str = ", ".join(f"{col_name}:{col_type}" for col_name, col_type in columns_with_id)

    # Выдаем сообщение, что таблица успешно создана
    print(f"\nТаблица '{table_name}' успешно создана со столбцами {columns_str}")
    return metadata

def drop_table(metadata, table_name):
    
    '''
    Удаляет таблицу из метаданных.
    Проверяет существование таблицы.
    Возвращает обновлённый словарь или выводит ошибку.
    '''
    
    # Проверяем существует ли такая таблица
    if table_name not in metadata:
        print(f"Ошибка: Таблица '{table_name}' не существует.")
        return
    
    # Если существует удаляем ее
    del metadata[table_name]
    print(f"\nТаблица '{table_name}' удалена.")
    return metadata


def list_tables(metadata):
    '''Выводит список таблиц в базе данных'''
    list_table_str = ', '.join(metadata.keys())
    # Выводим список таблиц
    print(f'\n Cписок таблиц: {list_table_str}')
