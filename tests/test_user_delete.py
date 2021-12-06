import allure

from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


@allure.epic("Delete users cases")
class TestUserDelete(BaseCase):

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Deleting a user for whom deletion is prohibited")
    def test_delete_blocked_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        # Авторизация
        response1 = MyRequests.post("/user/login", data=data)

        Assertions.assert_json_status_code(response1, 200)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        # Удаление пользователя, для которого удаление запрещено

        response2 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        Assertions.assert_json_status_code(response2, 400)
        assert response2.content.decode("utf-8") == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', \
            f"Unexpected response content {response2.content}"

    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("Deleting a user and checking that the user is deleted")
    def test_positive_delete_user(self):
        registration_data = self.prepare_registration_data()

        # Регистрация
        response1 = MyRequests.post("/user/", data=registration_data)

        Assertions.assert_json_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # Авторизация
        login_data = {
            'password': registration_data['password'],
            'email': registration_data['email']
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_json_status_code(response2, 200)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, 'x-csrf-token')
        user_id_from_auth_method = self.get_json_value(response2, "user_id")

        # Удаление пользователя

        response3 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        Assertions.assert_json_status_code(response3, 200)

        # Проверка удаления пользователя

        response4 = MyRequests.get(f"/user/{user_id_from_auth_method}")

        Assertions.assert_json_status_code(response4, 404)
        assert response4.content.decode("utf-8") == 'User not found', \
            f"Unexpected response content {response4.content}"

    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("Deleting a user while being authorized by another user")
    def test_negative_delete_user(self):
        registration_data = self.prepare_registration_data()

        name = registration_data['firstName']
        print(name)

        # Регистрация
        response1 = MyRequests.post("/user/", data=registration_data)

        Assertions.assert_json_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        # Авторизация пользователя, которого будем удалять
        login_data2 = {
            'password': registration_data['password'],
            'email': registration_data['email']
        }
        response2 = MyRequests.post("/user/login", data=login_data2)

        Assertions.assert_json_status_code(response2, 200)
        user_id_from_auth_method = self.get_json_value(response2, "user_id")

        # Регистрация пользователя для проверки удаления
        registration_data2 = self.prepare_registration_data()

        response3 = MyRequests.post("/user/", data=registration_data2)

        Assertions.assert_json_status_code(response3, 200)
        Assertions.assert_json_has_key(response3, "id")

        # Авторизация пользователя для проверки удаления
        login_data = {
            'password': registration_data2['password'],
            'email': registration_data2['email']
        }

        response4 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_json_status_code(response4, 200)

        auth_sid = self.get_cookie(response4, "auth_sid")
        token = self.get_header(response4, 'x-csrf-token')

        # Удаления пользователя
        response5 = MyRequests.delete(f"/user/{user_id_from_auth_method}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        # Проверка удаления пользователя
        response6 = MyRequests.get(f"/user/{user_id_from_auth_method}")

        print(response5.content)
        print(response5.text)
        print(response5.status_code)

        Assertions.assert_json_status_code(response6, 200)
        assert response6.content.decode("utf-8") == '{"username":"' + name + '"}', \
            f"Unexpected response content {response6.content}"
