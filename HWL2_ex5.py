import requests
methodList = ["GET", "POST", "DELETE", "PUT"]
for j in methodList:
    variableMethod = {"method": j}
    result = ""
    result = result + " GET " + requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params=variableMethod).text + ", "
    result = result + " POST " + requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data=variableMethod).text + ", "
    result = result + " PUT " + requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data=variableMethod).text + ", "
    result = result + " DELETE " + requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data=variableMethod).text
    if result.count("success") == 2:
        print("its method " + j + ":" + result)

