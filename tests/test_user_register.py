import allure
import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import random
import string

@allure.epic("Registration Cases")
class TestUserRegister(BaseCase):
    data_user = [
        {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'vinkotov@example.com'
        }]

    @allure.description("Registration users")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_json_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("Registration users with existing email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_json_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.description("Registration users with incorrect email")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_incorrect_email(self):
        letters = string.ascii_lowercase
        email = ''.join(random.choice(letters) for i in range(10)) + 'example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_json_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Invalid email format", \
            f"Unexpected response content {response.content}"

    @allure.description("Registration users with short name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_short_name(self):
        letters = string.ascii_lowercase
        firstName = random.choice(letters)

        data = self.prepare_registration_data(None, firstName)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_json_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'lastName' field is too short", \
            f"Unexpected response content {response.content}"

    @allure.description("Registration users with long name")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user_with_long_name(self):
        small_letters = string.ascii_lowercase
        up_letters = string.ascii_uppercase
        firstName = ''.join(random.choice(up_letters) + ''.join(random.choice(small_letters) for i in range(250)))

        data = self.prepare_registration_data(None, firstName)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_json_status_code(response, 400)
        assert response.content.decode("utf-8") == f"The value of 'lastName' field is too long", \
            f"Unexpected response content {response.content}"


    @allure.description("Checking the mandatory filling of all fields during registration")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.parametrize('data', data_user)
    def test_check_without_data(self, data):
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_json_status_code(response, 400)
        if 'password' not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: password", \
                f"Unexpected response content {response.content}"
        elif 'username' not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: username", \
                f"Unexpected response content {response.content}"
        elif 'firstName' not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: firstName", \
                f"Unexpected response content {response.content}"
        elif 'lastName' not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: lastName", \
                f"Unexpected response content {response.content}"
        elif 'email' not in data:
            assert response.content.decode("utf-8") == f"The following required params are missed: email", \
                f"Unexpected response content {response.content}"
