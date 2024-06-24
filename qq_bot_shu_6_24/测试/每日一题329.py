
import requests
url="https://api.lovelive.tools/api/SweetNothings/Web/1"
response=requests.get(url)
print(response.json()["returnObj"]["content"])