# src/primitive_db/parser.py

from src.primitive_db import decorators  # Импортируем декораторы


@decorators.handle_db_errors
def parse_insert_values(values_str):
    # Убираем скобки по краям
    values_str = values_str.strip('()').replace(',', '')
    values_list = values_str.split()

    value_pars = []
    for value in values_list:

        if value.startswith('"') and value.endswith('"'):
        # Убираем ковычки (первый и последний элемент)
            value = value[1:-1]
            value_pars.append(value)

        # Для двойных ковычек
        elif value.startswith("'") and value.endswith("'"):
            

        # Убираем ковычки (первый и последний элемент) 
            value = value[1:-1]
            value_pars.append(value)

        else:

        # Если нет ковычек пытаемся преобразовать в bool или int
        
            if value.isdigit(): # Проверяем состоит ли строка только из чисел
                value_pars.append(int(value))

        # Если строка не состоит из чисел, пытаемся преобразовать в bool
            elif value.lower() in ('true', 'yes', 'y', 't'):
                value_pars.append(True)
            elif value.lower() in ('false', 'no', 'n', 'f'):
                value_pars.append(False)
            else:
                # Если не число и не boolean 
                raise ValueError(f'\nСтроковое значение должно быть в кавычках: {value}')
                
    
              
    return(value_pars)
        


@decorators.handle_db_errors
def parse_where_set_clause(where_clause):
    
    '''
    Делает парсинг условия where_clause, определяет тип возвращаемых данных,
    используя наличие/отсутсвие кавычек
    '''

    if '=' not in where_clause:
        print('\nОшибка, отсутствует оператор =')
        return
    
    left, right = where_clause.split('=', 1)
    column = left.strip()
    value_str = right.strip()

    # Определяем тип по наличию ковычек у строковых значения:
    if value_str.startswith('"') and value_str.endswith('"'):
        
        # Убираем ковычки (первый и последний элемент)
        value = value_str[1:-1]

    # Для двойных ковычек
    elif value_str.startswith("'") and value_str.endswith("'"):

        # Убираем ковычки (первый и последний элемент) 
        value = value_str[1:-1]

    else:
        value = value_str
        # Если нет ковычек пытаемся преобразовать в bool или int
        
        if value_str.isdigit(): # Проверяем состоит ли строка только из чисел
            value = int(value_str)

        # Если строка не состоит из чисел, пытаемся преобразовать в bool
        elif value_str.lower() in ('true', 'yes', 'y', 't'):
            value = True
        elif value_str.lower() in ('false', 'no', 'n', 'f'):
            value = False
        else:
            # Если не число и не boolean - ОШИБКА (строка без кавычек)
            raise ValueError(f'\nСтроковое значение должно быть в кавычках: {value}')
            
    return {column: value}
    
 
  