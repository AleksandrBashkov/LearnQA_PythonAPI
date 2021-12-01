import requests
import pytest


class TestAgent:
    user_agents = [
        ("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30","Mobile","No","Android"),
        ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1","Mobile","Chrome","iOS"),
        ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)","Googlebot","Unknown","Unknown"),
        ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0","Web","Chrome","No"),
        ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1","Mobile","No","iPhone")
    ]
    @pytest.mark.parametrize("user_agent,expected_platform,expected_browser,expected_device", user_agents)
    def test_user_agent(self, user_agent, expected_platform, expected_browser, expected_device):
        url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
        data = {"User-Agent": user_agent}
        response = requests.get(url, headers=data)
        response_as_dict = response.json()
        assert response_as_dict["platform"] == expected_platform, "Ожидаемая платформа не соответствует фактической платформе из ответа"
        assert response_as_dict["browser"] == expected_browser, "Ожидаемый браузер не соответствует фактическому браузеру из ответа"
        assert response_as_dict["device"] == expected_device, "Ожидаемый девайс не соответствует фактическому девайсу из ответа"