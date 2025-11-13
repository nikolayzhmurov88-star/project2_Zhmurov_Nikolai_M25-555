# project2_Zhmurov_Nikolai_M25-555-

# Primitive DB
Простая реляционная база данных на Python с интерфейсом командной строки.

Описание:

- Primitive DB - это система управления базами данных, которая позволяет:

- Создавать и удалять таблицы

- Работать с различными типами данных

- Выполнять базовые операции с данными

- Сохранять метаданные в JSON-формате

- Сохранять данный таблицы в JSON-формате

- Полная поддержка CRUD команд

- Обработка ошибок

- Подтверждение операции удаления

- Кеширование запросов

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
database

# Основные команды
Работа с таблицами:

insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись."

select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию."

select from <имя_таблицы> - прочитать все записи."

update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись."

delete from <имя_таблицы> where <столбец> = <значение> - удалить запись."

info <имя_таблицы> - вывести информацию о таблице."

create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ... - создать таблицу

list_tables - показать список всех таблиц

drop_table <имя_таблицы> - удалить таблицу

Общие команды:

exit - выход из программы

help - справочная информация


Демонстрация работы:
https://asciinema.org/a/iltgghcuQxzB1RGBFA4wxFmv9

Демонстрация работы CRUD команд:
https://asciinema.org/a/TdA7EMSGPLx8wOBbEipVfY1DD

Итоговая демонстрация программы:



# Команды для тестирования:

create_table people name:str sex:str age:int prof:bool
create_table cars brabd:str model:str year:int available:bool

insert into people values 'Pavel', 'male', 34, true 
insert into people values 'Lena', 'female', 22, true 
insert into people values 'Alexander', 'male', 37, false 
insert into people values 'Oksana', 'female', 65, true 

insert into cars values 'Honda', 'civic', 2007, true 
insert into cars values 'Toyota', 'corolla', 2021, false 

select from people
select from cars

select from people where sex = 'female'
select from people where prof = true
select from cars where year = 2007 
select from cars where model = 'civic'
select from cars where model = civic

update people set name = Sveta where age = 22
update people set name = 'Sveta' where age = 22
select from people

update cars set model = 'Accord' where year = 2007
select from car
select from cars

select from people
delete from people where prof = false
select from people

info people
info cars

