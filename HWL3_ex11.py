import requests
import json

class TestGetCookie:
    def test_get_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        print(response.cookies.get_dict())
        param1 = {'HomeWork': 'hw_value'}
        param2 = response.cookies.get_dict()
        assert json.dumps(param1) == json.dumps(param2), "Получен неверный куки"


