import requests

url = "https://api.52vmy.cn/api/img/tu/girl"
response = requests.get(url)
data = response.json()
url_3 = data['url']
print((url_3))
response = requests.get(url_3)
response = response.content
with open("群聊\\suijitu.jpg", "wb") as f:
    f.write(response)