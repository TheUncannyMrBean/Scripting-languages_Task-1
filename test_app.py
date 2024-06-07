import unittest
import json
from io import BytesIO
from app import application

class TestApp(unittest.TestCase):

    def test_get_gmt_time(self):
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/',
        }
        response_body = self.call_app(environ)
        self.assertIn('GMT', response_body)

    def test_get_timezone_time(self):
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/Europe/Moscow',
        }
        response_body = self.call_app(environ)
        self.assertIn('Europe/Moscow', response_body)

    def test_post_convert_time(self):
        environ = {
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': '/api/v1/convert',
            'CONTENT_LENGTH': str(len(json.dumps({
                "date": "12.20.2021 22:21:05", "tz": "EST", "target_tz": "Europe/Moscow"
            }))),
            'wsgi.input': BytesIO(json.dumps({
                "date": "12.20.2021 22:21:05", "tz": "EST", "target_tz": "Europe/Moscow"
            }).encode('utf-8'))
        }
        response_body = self.call_app(environ)
        self.assertIn('converted_time', response_body)

    def test_post_datediff(self):
        environ = {
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': '/api/v1/datediff',
            'CONTENT_LENGTH': str(len(json.dumps({
                "first_date": "12.06.2024 22:21:05", "first_tz": "EST",
                "second_date": "12:30pm 2024-02-01", "second_tz": "Europe/Moscow"
            }))),
            'wsgi.input': BytesIO(json.dumps({
                "first_date": "12.06.2024 22:21:05", "first_tz": "EST",
                "second_date": "12:30pm 2024-02-01", "second_tz": "Europe/Moscow"
            }).encode('utf-8'))
        }
        response_body = self.call_app(environ)
        self.assertIn('seconds_diff', response_body)

    def test_invalid_timezone(self):
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': '/Invalid/Timezone',
        }
        response_body = self.call_app(environ)
        self.assertIn('Некорректная временная зона', json.loads(response_body)['error'])

    def test_invalid_date_format(self):
        environ = {
            'REQUEST_METHOD': 'POST',
            'PATH_INFO': '/api/v1/convert',
            'CONTENT_LENGTH': str(len(json.dumps({
                "date": "invalid-date", "tz": "EST", "target_tz": "Europe/Moscow"
            }))),
            'wsgi.input': BytesIO(json.dumps({
                "date": "invalid-date", "tz": "EST", "target_tz": "Europe/Moscow"
            }).encode('utf-8'))
        }
        response_body = self.call_app(environ)
        self.assertIn('Некорректные данные для преобразования', json.loads(response_body)['error'])

    def call_app(self, environ):
        def start_response(status, response_headers):
            self.status = status
            self.response_headers = response_headers
        
        result = application(environ, start_response)
        response_body = b''.join(result).decode('utf-8')
        return response_body

if __name__ == '__main__':
    unittest.main()
