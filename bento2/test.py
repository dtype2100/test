import json
import requests

response = requests.post(
   "http://0.0.0.1:3000/classify",
   data="[[5.9, 3, 5.1, 1.8]]",
).text

print(response.json())