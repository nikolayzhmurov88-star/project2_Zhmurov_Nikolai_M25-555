# src/primitive_db/engine.py

# Импортируем библиотеку prompt, shlexv и модули utils и core
import prompt
import shlex
from src.primitive_db import utils
from src.primitive_db import core

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



def run():
    metadata_file = "db_meta.json"

    while True:
        metadata = utils.load_metadata(metadata_file)

        try:
            user_input = input("\n>>>Введите команду: ")
            if user_input:
                args = shlex.split(user_input)
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
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")



# Вызываем ее только при запуске модуля как программы
if __name__ == "__main__":
    run()