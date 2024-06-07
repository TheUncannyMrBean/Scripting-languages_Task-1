import json
from datetime import datetime
import pytz
from pytz import timezone
from wsgiref.simple_server import make_server

# Функция для получения текущего времени в заданной временной зоне
def get_time_in_tz(tz_name="GMT"):
    tz = timezone(tz_name)
    time_in_tz = datetime.now(tz)
    return time_in_tz.strftime("%Y-%m-%d %H:%M:%S %Z%z")

# Функция для преобразования времени из одной временной зоны в другую
def convert_time(data, target_tz):
    try:
        source_tz = timezone(data['tz'])
        target_tz = timezone(target_tz)
        date_time = datetime.strptime(data['date'], "%m.%d.%Y %H:%M:%S")
        source_time = source_tz.localize(date_time)
        target_time = source_time.astimezone(target_tz)
        return target_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    except Exception as e:
        raise ValueError(f"Некорректные данные для преобразования: {str(e)}")

# Функция для вычисления разницы в секундах между двумя датами в разных временных зонах
def datediff(data):
    try:
        first_tz = timezone(data['first_tz'])
        second_tz = timezone(data['second_tz'])
        first_date = datetime.strptime(data['first_date'], "%m.%d.%Y %H:%M:%S")
        second_date = datetime.strptime(data['second_date'], "%I:%M%p %Y-%m-%d")
        
        first_date = first_tz.localize(first_date)
        second_date = second_tz.localize(second_date)
        
        diff = second_date - first_date
        return int(diff.total_seconds())
    except Exception as e:
        raise ValueError(f"Некорректные данные для вычисления разницы между датами: {str(e)}")

# Вспомогательная функция для обработки ошибок
def handle_error(start_response, status, message):
    response_body = json.dumps({"error": message})
    start_response(status, [('Content-Type', 'application/json')])
    return [response_body.encode('utf-8')]

# Основная функция WSGI-приложения
def application(environ, start_response):
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', 'GET')

    try:
        if method == 'GET' and path.startswith('/'):
            tz_name = path[1:] if len(path) > 1 else 'GMT'
            try:
                current_time = get_time_in_tz(tz_name)
                response_body = f"<html><body><h1>Текущее время в {tz_name}: {current_time}</h1></body></html>"
                start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
            except pytz.UnknownTimeZoneError:
                return handle_error(start_response, '400 Bad Request', 'Некорректная временная зона')

        elif method == 'POST' and path == '/api/v1/convert':
            try:
                request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
                data = json.loads(request_body)
                target_tz = data['target_tz']
                converted_time = convert_time(data, target_tz)
                response_body = json.dumps({"converted_time": converted_time})
                start_response('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
            except (ValueError, KeyError) as e:
                return handle_error(start_response, '400 Bad Request', str(e))

        elif method == 'POST' and path == '/api/v1/datediff':
            try:
                request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))).decode('utf-8')
                data = json.loads(request_body)
                seconds_diff = datediff(data)
                response_body = json.dumps({"seconds_diff": seconds_diff})
                start_response('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
            except (ValueError, KeyError) as e:
                return handle_error(start_response, '400 Bad Request', str(e))

        else:
            return handle_error(start_response, '404 Not Found', 'Ресурс не найден')

        return [response_body.encode('utf-8')]
    
    except Exception as e:
        return handle_error(start_response, '500 Internal Server Error', str(e))

if __name__ == '__main__':
    with make_server('', 8000, application) as httpd:
        print("Сервер запущен на порту 8000...")
        httpd.serve_forever()
