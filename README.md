# Primitive Database
Консольное приложение для управления простой базой данных.

## Установка

```bash
make install
make build
make package-install

## Команды:

create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ... - создать таблицу

list_tables - показать список всех таблиц

drop_table <имя_таблицы> - удалить таблицу

exit - выход из программы

help - справочная информация

## Пример использования 

>>>Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>>Введите команду: create_table users name:str
Ошибка: Таблица "users" уже существует.

>>>Введите команду: list_tables
- users

>>>Введите команду: drop_table users
Таблица "users" успешно удалена.

>>>Введите команду: drop_table products
Ошибка: Таблица "products" не существует.

>>>Введите команду: help
***Процесс работы с таблицей***
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> exit - выход из программы
<command> help - справочная информация  

## Демонстрация работы базы данных

Запуск базы данных, создание, проверка и удаление таблицы:

https://asciinema.org/a/9zZZiJ7grd8A9LfpPUGAE3RWa

## CRUD-операции

<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.
<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.
<command> select from <имя_таблицы> - прочитать все записи.
<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.
<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.
<command> info <имя_таблицы> - вывести информацию о таблице.

## Демонстрация операций с данными 

https://asciinema.org/a/iPZoGLbg5FrzDY5ooL6yrcQQu

## Обработка ошибок и подтверждение операции 

- Автоматическая обработка ошибок через декоратор `@handle_db_errors`
- Интерактивное подтверждение через декоратор `@confirm_action` 

## Демонстрация декораторов 

https://asciinema.org/a/QeUaRofrfrieVWensdj5CMrI8


