# Тестовое задание **Valiotti Analytics**

## Задача №1
Имеется таблица `city_population` с населением городов: 
- `city` (наименование города), 
- `population` (численность населения).
Необходимо написать запрос, который выводит город с минимальным населением.

[Результат](https://github.com/aeksei/valiotti_test/blob/master/first.sql) — скрипт в формате `.sql`

## Задача №2
Есть таблица пользователей `user` (`user_id` — id пользователя, `installed_at` — дата установки) и таблица активности 
`client_session` (`user_id`, `created_at` — таймстемп активности).  
Необходимо написать SQL-запрос который считает **Retention** 1, 3, 7 дня по пользователям с группировкой установок 
по месяцам (с января 2020-го года). 

[Результат](https://github.com/aeksei/valiotti_test/blob/master/second.sql) — скрипт в формате `.sql`

## Задача №3. 
Скрипт на Python.  
Необходимо написать код на Python. Скрипт обращается к API amoCRM и забирает последние 30 сделок, 
сохраняет их в pandas dataframe. 

[Результат](https://github.com/aeksei/valiotti_test/blob/master/main.py) - `.py`-скрипт
