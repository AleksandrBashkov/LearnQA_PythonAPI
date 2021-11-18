import json
import time
import requests


url = "https://playground.learnqa.ru/ajax/api/longtime_job"
response = requests.get(url)
str_response = response.json()
print(str_response["token"])


response1 = requests.get(url, params=str_response)
str_response1 = response1.json()
if "Job is NOT ready" in str_response1["status"]:
    print("Задача не выполнена")
    time.sleep(15)
    response2 = requests.get(url, params=str_response)
    str_response2 = response2.json()
    print(str_response2)
    if "Job is ready" in str_response2["status"] and "42" in str_response2["result"]:
        print("Задача завершена")
else:
    print("Задача выполнилась быстрее проверки")
