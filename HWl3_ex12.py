import requests
import json
import pytest

class TestGetHeader:
    def test_get_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)

        param1 = response.headers["Date"]
        param2 = response.headers["Expires"]
        assert param1 == param2, "Получены неверные заголовки"
