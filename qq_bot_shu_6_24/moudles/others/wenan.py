import requests
def Kfc():
    url="https://api.shadiao.pro/kfc"
    response=requests.get(url)
    print(response.json()["data"]["text"])