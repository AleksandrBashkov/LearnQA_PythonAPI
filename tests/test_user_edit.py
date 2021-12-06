import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import time
from datetime import datetime


@allure.epic("Update data users cases")
class TestUserEdit(BaseCase):

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Name change and change check")
    def test_edit_just_create_user(self):
        # Регистрация
        register_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_json_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Логин
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Изменение
        new_name = "Change Name"

        response3 = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})
        Assertions.assert_json_status_code(response3, 200)

        # Получение данных
        response4 = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Changing data under an unauthorized username")
    def test_edit_no_authorization(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        new_email = f"{base_part}{random_part}@{domain}"

        response = MyRequests.put(f"/user/2", data={"email": new_email})

        Assertions.assert_json_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Auth token not supplied", \
            f"Unexpected response content {response.content}"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Change user data, being authorized by another user")
    def test_edit_authorization_another_user(self):
        # Регистраци
        registration_data = self.prepare_registration_data()

        response1 = MyRequests.post("/user/", data=registration_data)

        Assertions.assert_json_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        time.sleep(1)

        # Регистрация пользователя для редактирования
        registration_data2 = self.prepare_registration_data()

        response2 = MyRequests.post("/user/", data=registration_data2)

        Assertions.assert_json_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        old_name = registration_data2['firstName']
        old_last_name = registration_data2['lastName']
        user_id = self.get_json_value(response2, "id")

        # Авторизация пользователя пытающегося изменить другого пользователя
        login_data = {
            'password': registration_data['password'],
            'email': registration_data['email']
        }

        response3 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, 'x-csrf-token')

        # Редактирование пользователя
        new_first_name = "Changed Name"
        new_last_name = "Changed LastName"
        response4 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_first_name, "lastName": new_last_name}
                                   )

        Assertions.assert_json_status_code(response4, 200)

        # Авторизация измененного пользователя
        login_data2 = {
            'password': registration_data2['password'],
            'email': registration_data2['email']
        }

        response5 = MyRequests.post("/user/login", data=login_data2)

        auth_sid2 = self.get_cookie(response5, "auth_sid")
        token2 = self.get_header(response5, 'x-csrf-token')

        Assertions.assert_json_status_code(response5, 200)

        # Проверка изменений
        response6 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token2},
                                   cookies={"auth_sid": auth_sid2}
                                   )

        Assertions.assert_json_value_by_name(
            response6,
            "firstName",
            old_name,
            "Wrong name of the User after edit"
        )
        Assertions.assert_json_value_by_name(
            response6,
            "lastName",
            old_last_name,
            "Wrong lastName of the User after edit"
        )

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Сhange the user's email, being authorized by the same user, to a new email without the @ symbol")
    def test_edit_email_to_wrong_by_authorized_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_json_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_email = "1example.com"
        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"email": new_email}
                                   )
        Assertions.assert_json_status_code(response3, 400)
        assert response3.content.decode("utf-8") == f"Invalid email format"

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Сhange the firstName of the user, being authorized by the same user, to a very short value of one character")
    def test_edit_user_by_short_firstname(self):
        # Регистрация
        registration_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=registration_data)

        Assertions.assert_json_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        # Авторизация
        login_data = {
            'password': registration_data['password'],
            'email': registration_data['email']
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, 'x-csrf-token')

        # Изменение пользователя
        new_name = "A"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name}
                                   )

        Assertions.assert_json_status_code(response3, 400)
        assert response3.content.decode("utf-8") == '{"error":"Too short value for field firstName"}', \
            f"Unexpected response content {response3.content}"
