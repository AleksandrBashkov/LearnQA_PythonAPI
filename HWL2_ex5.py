import json


json_text = json.loads('{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}')

for i in json_text['messages']:
    if 'second message' in i['message']:
        print(i['message'])

