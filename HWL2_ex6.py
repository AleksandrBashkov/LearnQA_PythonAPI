import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
response_url = response.history[0]

length_redirect = len(response.history)
last_response = response.history[-1]
print(last_response.url)
print(length_redirect)




