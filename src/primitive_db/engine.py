# src/primitive_db/engine.py

# Импортируем библиотеку prompt, shlexv и модули utils и core
import prompt
import shlex
from src.primitive_db import utils
from src.primitive_db import core
from src.primitive_db import parser
'''
# Функция приветсвия
def welcome():
    print("\nПервая попытка запустить проект!")
    print("\n*** \\<command> exit - выйти из программы")
    print("\n*** \\<command> help - справочная информация")
    while True:
        try:
            cmd = prompt.string("\nВведите команду: ").strip()
            if cmd == "exit":
                print("\nВыход из программы.")
                break
            elif cmd == "help":
                print("\n*** \\<command> exit - выйти из программы")
                print("\n*** \\<command> help - справочная информация")
            else:
                print(f"\nНеверная команда: {cmd}")
        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break
'''


def run():
    metadata_file = "db_meta.json"

    while True:
        metadata = utils.load_metadata(metadata_file)

        try:
            user_input = input("\n>>>Введите команду: ")
            if user_input:
                
                args = user_input.split()
                command = args[0].lower()
                
                
                match command:
                    case 'create_table':
                    
                        # Если количество слов в команде меньше 3, занчит пользователь неверно ввел команду 
                        if len(args) < 3:
                            print("Ошибка: используйте create_table <table_name> <col1:type1> <col2:type2> ...")
                            continue

                        # Определяем имя создаваемой таблицы
                        table_name = args[1]

                        # Определяем солонки таблицы
                        cols_args = args[2:]

                        # Проверяем правильно ли заданы столбцы таблицы
                        columns = []
                    
                        # Если в элементах списка, соответсвующих столбцам нет ':'выводим ошибку
                        for ct in cols_args:
                            if ':' not in ct:
                                print(f"Неверный формат столбца '{ct}', ожидается name:type")
                                continue
                            # Разделяем элемент списка (команды) на имя столбца и тип столбца    
                            name, typ = ct.split(':', 1)
                            columns.append((name, typ))
                    
                        # Вызываем функцию добавления таблицы
                        metadata = core.create_table(metadata, table_name, columns)
                    
                        # Если добавление успешно, то сохраняем в файл
                        if metadata is not None:
                            utils.save_metadata(metadata_file, metadata)

                    # Удаление таблицы
                    case 'drop_table':
                    
                        # Проверяем, что количество слов в команде равно 2
                        if len(args) != 2:
                            print("\nОшибка: используйте drop_table <table_name>")
                            continue
                    
                        # Определяем имя таблицы, как элемент списка команды с индексом 1
                        table_name = args[1]

                        # Меняем базу данных вызывая функцию удаления таблицы
                        metadata = core.drop_table(metadata, table_name)

                        # Сохраняем измененную базу данных если удаление выполнено успешно
                        if metadata is not None:
                            utils.save_metadata(metadata_file, metadata)

                    # Список таблиц
                    case 'list_tables':
                        if len(args) != 1:
                            print(f'\nФункция list_tables не требует ввода значений. Лишние значения {', '.join(args[1:])}')
                            continue
                        # Вызываем функцию вывода списка таблиц
                        core.list_tables(metadata)
                        
                
                     # Выход из программы
                    case 'exit':
                        if len(args) != 1:
                            print(f'\nФункция exit не требует ввода значений. Лишние значения {', '.join(args[1:])}')
                            continue
                        print("\nВыход из программы.")
                        break

                    # Вывод списка команд
                    case 'help':
                        if len(args) != 1:
                            print(f'\nФункция help не требует ввода значений. Лишние значения {', '.join(args[1:])}')
                            continue
                        print_help()

                    # Добавление записи в таблицу
                    case 'insert':
                        if len(args) >= 5 and args[1] == 'into' and args[3] == 'values':
                            
                            # Определяем имя таблицы в которую добавляем строки
                            table_name = args[2]
    
                            # Объединяем оставшуюся часть списка в строку
                            values_str = ' '.join(args[4:])

                            # Вызываем функцию парсинга команд
                            values_str = parser.parse_insert_values(values_str)

                            # Вызываем функцию добавления записи     
                            core.insert(metadata, table_name, values_str)

                        else:
                            print('Неверная команда, правильно "insert into <Имя таблицы> values ...." ')
    

                    # Фильтрация таблицы
                    case 'select':
                        if len(args) == 3 and args[1] == 'from':
                            where_clause = None
                            table_name = args[2]
                            # Определяем имя таблицы c которой будем работать

                            if table_name in metadata:

                                # Загружаем данные таблицы
                                table_data = utils.load_table_data(table_name)

                                # Вызываем функцию фильтрации таблицы
                                core.select(table_data, where_clause)
                            
                            else:
                                print('\nТакой таблицы не существует')
                            
                        elif len(args) == 7 and args[1] == 'from' and args[3] == "where":
                            
                            table_name = args[2]
                            # Определяем имя таблицы c которой будем работать
                            if table_name in metadata:

                                # Загружаем данные таблицы
                                table_data = utils.load_table_data(table_name)

                                # Объединяем оставшуюся часть списка в строку
                                where_clause = ' '.join(args[4:])

                                # Вызываем функцию парсинга команд
                                where_clause = parser.parse_where_set_clause(where_clause)

                                # Вызываем функцию фильтрации таблицы
                                core.select(table_data, where_clause)
                            
                            else:
                                print('\nТакой таблицы не существует')
                                    
                                
                                # Вызываем функцию фильтрации таблицы
                                
                                core.select(table_data, where_clause)
                        else:
                            print('\nНеверная команда, правильно: select from <имя_таблицы> where <столбец> = <значение>')
                    
                        
                    
                    # Изменение таблицы
                    case 'update':
                        # Делаем первичную проверку команды по количеству элементов списка
                        if len(args) == 10 and args[2] == 'set' and args[6] == 'where':
                           
                            # Определяем имя таблицы c которой будем работать
                            table_name = args[1]

                            # Загружаем данные таблицы
                            table_data = utils.load_table_data(table_name)

                            # !!!Временно присваиваем  where_clause и set_clause постоянные значения!!!
                            
                            # Определяем элементы списка, отвечающие за условия и конвертируем в строки
                            where_clause = ' '.join(args[7:10])
                            set_clause = ' '.join(args[3:6])
                            
                            # Вызываем функцию для парсинга
                            where_clause = parser.parse_where_set_clause(where_clause)
                            set_clause = parser.parse_where_set_clause(set_clause)
                            
                            # Вызываем функцию изменения таблицы
                            if where_clause and set_clause:
                                core.update(table_data, set_clause, where_clause)

                                # Записываем измененную таблицу в файл
                                utils.save_table_data(table_name, table_data)
                            
                        else:
                            print('Неверный ввод команды, правильно: update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия>')
                            return
                     

                    # Удаление записей из таблицы
                    case 'delete':
                        
                        # Делаем первичную проверку команды по количеству элементов списка
                        if len(args) == 7 and args[1] == 'from' and args[3] == 'where':
                            
                            # Определяем имя таблицы c которой будем работать
                            table_name = args[2]

                            # Загружаем данные таблицы
                            table_data = utils.load_table_data(table_name)

                            # !!!Временно присваиваем  where_clause и set_clause постоянные значения!!!
                            
                            # Определяем элементы списка, отвечающие за условие и конвертируем в строку
                            where_clause = ' '.join(args[4:7])
                            
                            # Вызываем функцию для парсинга
                            where_clause = parser.parse_where_set_clause(where_clause)
                            
                            # Вызываем функцию изменения таблицы
                            core.delete(table_data, where_clause)

                            # Записываем измененную таблицу в файл
                            utils.save_table_data(table_name, table_data)
                        else:
                            print('Неверный ввод команды, правильно: delete from <имя_таблицы> where <столбец> = <значение>')
                

                    case 'info':
                        if len(args) == 2:
                            # Определяем имя таблицы c которой будем работать
                            table_name = args[1]

                            # Загружаем файл с таблицей
                            table_data = utils.load_table_data(table_name)

                            # Вызываем функцию вывода информации о таблице
                            core.info(table_data, metadata, table_name)
                        else: 
                            print('Неверно введена команда info, правильно: info <имя_таблицы>')


                    # Неизвестная команда 

                    case _:
                        print(f"\nФункции {command} нет. Попробуйте снова. ")
            else:
                print('\nВы не ввели команду!')

        except KeyboardInterrupt:
            print("\nВыход из программы.")
            break
            
          



# Функция помощи
def print_help():
    """Prints the help message for the current mode."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")



# Вызываем ее только при запуске модуля как программы
if __name__ == "__main__":
    run()