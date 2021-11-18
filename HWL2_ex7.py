import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"  #1 пункт
response_get = requests.get(url)
print(response_get.text)

response_nonexistent = requests.head(url)  #2 пункт задания
print(response_nonexistent.text)

methodList = ["GET", "POST", "DELETE", "PUT"]  #3 пункт
for i in methodList:
    i = requests.request(method=methodList[0], url="https://playground.learnqa.ru/ajax/api/compare_query_type")
    print(i.text)

#4 пункт
for j in methodList:
    variableMethod = {"method": j}
    result = ""
    result = result + " GET " + requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=variableMethod).text + ", "
    result = result + " POST " + requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=variableMethod).text + ", "
    result = result + " PUT " + requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=variableMethod).text + ", "
    result = result + " DELETE " + requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=variableMethod).text
    if result.count("success") == 2:
        print("its method " + j + ":" + result)









