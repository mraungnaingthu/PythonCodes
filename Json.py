import json

data = '{"name": "Robert", "email": "robert@gmail.com", "password": "robert123"}'

api = json.loads(data)
print(api)
print(type(api))