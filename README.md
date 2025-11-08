# project2_Zhmurov_Nikolai_M25-555-

# Primitive DB
Простая реляционная база данных на Python с интерфейсом командной строки.

Описание:

- Primitive DB - это система управления базами данных, которая позволяет:

- Создавать и удалять таблицы

- Работать с различными типами данных

- Выполнять базовые операции с данными

- Сохранять метаданные в JSON-формате

# Установка и сборка

# Клонируйте репозиторий
git clone https://github.com/nikolayzhmurov88-star/project2_Zhmurov_Nikolai_M25-555.git
cd project2_Zhmurov_Nikolai_M25-555

# Установите зависимости и соберите пакет
make install
make build

# Установите собранный wheel-пакет
make package-install

# Теперь можно запускать из любого места
poetry database

# Основные команды
Работа с таблицами:

create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ... - создать таблицу

list_tables - показать список всех таблиц

drop_table <имя_таблицы> - удалить таблицу

Общие команды:

exit - выход из программы

help - справочная информация


Демонстрация работы:
https://asciinema.org/a/iltgghcuQxzB1RGBFA4wxFmv9