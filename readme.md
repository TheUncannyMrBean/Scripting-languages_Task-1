
# WSGI Time Service Application

## Описание

Это WSGI-приложение предоставляет сервис для работы с датами и временными зонами, аналогичный сервису time.is. Оно реализует следующие функции:

1.  **GET /<tz name>**: Отдает текущее время в запрошенной временной зоне в формате HTML. Если `<tz name>` пустой, возвращает время в GMT.
2.  **POST /api/v1/convert**: Преобразует дату и время из одного часового пояса в другой.
3.  **POST /api/v1/datediff**: Возвращает число секунд между двумя датами из параметра data.

## Установка

1.  Клонируйте репозиторий:
    
    `git clone git@github.com:TheUncannyMrBean/Scripting-languages_Task-1.git` 
    
2.  Установите необходимые зависимости:
    
    `pip install pytz` 
    

## Запуск

Вы можете запустить приложение с использованием `wsgiref.simple_server`:

`python app.py` 

Приложение будет доступно по адресу `http://127.0.0.1:8000`.

## Примеры использования

### 1. Получение текущего времени в заданной временной зоне

**GET /<tz name>**

Пример:

`GET http://127.0.0.1:8000/Europe/Moscow` 

Если `<tz name>` пустой:

`GET http://127.0.0.1:8000/` 

### 2. Преобразование даты и времени из одного часового пояса в другой

**POST /api/v1/convert**

Тело запроса (JSON):

`{
    "date": "12.20.2021 22:21:05",
    "tz": "EST",
    "target_tz": "Europe/Moscow"
}` 

Пример запроса:


`POST http://127.0.0.1:8000/api/v1/convert
Content-Type: application/json

{
    "date": "12.20.2021 22:21:05",
    "tz": "EST",
    "target_tz": "Europe/Moscow"
}` 

### 3. Вычисление разницы во времени между двумя датами

**POST /api/v1/datediff**

`{
    "first_date": "12.06.2024 22:21:05",
    "first_tz": "EST",
    "second_date": "12:30pm 2024-02-01",
    "second_tz": "Europe/Moscow"
}` 

Пример запроса:

`POST http://127.0.0.1:8000/api/v1/datediff
Content-Type: application/json

{
    "first_date": "12.06.2024 22:21:05",
    "first_tz": "EST",
    "second_date": "12:30pm 2024-02-01",
    "second_tz": "Europe/Moscow"
}` 

## Тестирование

Запустите тесты, чтобы убедиться, что все работает корректно:

`python test_app.py` 

## Postman

Для удобного тестирования API, вы можете использовать коллекцию запросов Postman. Ссылка на коллекцию:

[Коллекция Postman](https://www.postman.com/solar-capsule-541174-1083/workspace/workspace/request/24733693-1cf72380-64bf-43df-a590-a5f5170ebc2d)
