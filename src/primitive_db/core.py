# src/primitive_db/core.py

# Импортируем utils для вызова функций загрузки и сохранения таблиц
from src.primitive_db import utils

# Имопртируем PrettyTable
from prettytable import PrettyTable

# Импортируем декораторы
from src.primitive_db import decorators


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


@decorators.log_time
def insert(metadata, table_name, values):

    '''
    Вставляет новую запись в таблицу.
    '''

    # Проверяем существование таблицы
    if table_name not in metadata:
        print(f"\nОшибка: Таблица '{table_name}' не существует")
        return metadata
    
    # Получаем список столбцов и типов данных в таблице
    table_data = metadata[table_name]

    # Считываем данные таблицы из файла, либо создаем файл
    data = utils.load_table_data(table_name)
    utils.save_table_data(table_name, data)
   
    
    # Проверяем количество значений
    if len(values) != len(table_data) - 1:
        print(f"\nОшибка: Ожидается {len(table_data) - 1} значений(я), получено {len(values)}")
        return metadata
    
    # Определяем список столбцов таблицы без первого (ID)
    table_data_ID = table_data[1:]
    
    # Создаем список только с типами данных (списковое включение)
    types = [typ[1] for typ in table_data_ID]

    # Делаем проверку данных, конвертацию не делаем, така как она сделана на этапе парсинга
    # Создаем цикл где попарно пребиараем пары значение - тип
    for value, col_type in zip(values, types):
        if type(value).__name__  != col_type:
            print(type(value).__name__ )
            print(col_type)
            print('\nОшибка: несоответсвие типов данных {value} не {col_type}')
            return
    
    if data:
        max_id = max(item["ID"] for item in data)
        new_id = max_id + 1

    else:
        new_id = 1
            
    # Создаем список столбцов таблицы без типов данных 
    names = [nam[0] for nam in table_data]

    # Создаем новую запись
    new_record = dict(zip(names, [new_id] + values))
  
    # Добавляем запись в таблицу
    data.append(new_record)
    print(f"\nЗапись добавлена в таблицу '{table_name}' с ID {new_id}")
    utils.save_table_data(table_name, data)


@decorators.log_time
def select(table_data, where_clause=None):

    '''
    Если where_clause не задан, возвращает все данные.
    Если задан, фильтрует и возвращает только подходящие записи.
    '''

    # Создаём таблицу с заголовками из ключей первого словаря
    table = PrettyTable(field_names=list(table_data[0].keys()))

      
    # Если where_clause передан фильтруем таблицу
    if where_clause:
        
        # Создаём таблицу с заголовками из ключей первого словаря
        table = PrettyTable(field_names=list(table_data[0].keys()))

        # Делим словарь на ключ и значание
        key = list(where_clause.keys())[0]
        value = list(where_clause.values())[0]
        

        if key in table_data[0].keys():
           
            i = 0
            # Перебираем словари каждой строки
            for row in table_data:
            
                # Обращаемся в каждой строке к ключу и сравниваем значения
                if row.get(key) == value:
                    # Добавляем строки в объект PrettyTable
                    table.add_row(list(row.values()))
                    i += 1
            if i:
                print('\nТаблица отфильтрована')
                print(table)
            
            if not i:
                for row in table_data:
                    table.add_row(list(row.values()))
                print(table)
                print(f"\nВ этой таблице нет значений с {str(where_clause)[1:-1]} выведена вся таблица")
        
        else:
            print(f'\nСтолбца {key} в таблице нет')
    
                   
    else:

        # Добавляем строки - значения из каждого словаря
        for row in table_data:

            # Добавляем все строки в объект PrettyTable
            table.add_row(list(row.values()))
        print(table)
        print('\nУсловие фильтрации не задано, выведена полная таблица')

        
            
        

def update(table_data, set_clause, where_clause):

    '''
    Находит записи по where_clause.
    Обновляет в найденных записях поля согласно set_clause.
    Возвращает измененные данные.
    '''

    # Делим словарь на ключ и значание
    key_wc = list(where_clause.keys())[0]
    value_wc= list(where_clause.values())[0]
    
    key_sc = list(set_clause.keys())[0]
    value_sc= list(set_clause.values())[0]

    changed_id = []
    # Перебираем словари каждой строки
    for row in table_data:

        # Обращаемся в каждой строке к ключу и сравниваем значения
        if row.get(key_wc) == value_wc:
            row[key_sc] = value_sc

            # Фиксируем номера измененных ID или одного ID
            changed_id.append(row['ID'])


    if changed_id:
        # Выводим сообщение об успешном изменении таблицы       
        print(f"\nЗапись с ID = {(', ').join(map(str,changed_id))} в успешно обновлена")
    else:
        print(f"\nЗапись(си) с условием {str(where_clause)[1:-1]} не найдена в данной таблице")

    return table_data



def delete(table_data, where_clause):

    '''
    Находит записи по where_clause и удаляет их.
    Возвращает измененные данные.
    '''

   # Делим словарь на ключ и значание
    key_wc = list(where_clause.keys())[0]
    value_wc= list(where_clause.values())[0]
    
    changed_id = []
    i = 0
    # Перебираем словари каждой строки
    for row in table_data:
        
        # Обращаемся в каждой строке к ключу и сравниваем значения
        if row.get(key_wc) == value_wc:

            
            # Фиксируем номера удаленных ID
            changed_id.append(row['ID'])

            # Если строка удовлетворяет требованиям, удаляем ее
            del table_data[i]
        i += 1
    
    if changed_id:
        # Выводим сообщение об успешном изменении таблицы       
        print(f"\nЗапись(си) с ID = {(', ').join(map(str,changed_id))} в успешно удалена(ы)")

    else:
        print(f"\nЗапись(си) с условием {str(where_clause)[1:-1]} не найдена в данной таблице")
    


    return table_data

def info(table_data, metadata, table_name):
    if table_name not in metadata:
        print(f"\nОшибка: Таблица '{table_name}' не существует")
        return metadata
    
    print(f'\nТаблица: {table_name}')

    # Списковое включение
    columns = ', '.join([f"{col}:{typ}" for col, typ in metadata[table_name]])
    print(f'\nСтолбцы: {columns}')
    print(f'\nКоличество записей: {len(table_data)}')
