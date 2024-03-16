import SparkApi

# 以下密钥信息从控制台获取
appid = "fe98a5ed"  # 填写控制台中获取的 APPID 信息
api_secret = "MjNhYTM5MmFkYzE4ODlmZThjMTM5NmYx"  # 填写控制台中获取的 APISecret 信息
api_key = "c88336e5cd24146460de17f4a8f31ef1"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“general/generalv2”
domain = "generalv3"  # v3.0版本
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址

text = []


# length = 0

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text

def ai_bot_message_back(Input):
    text.clear()
    question = checklen(getText("user", Input))
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    getText("assistant", SparkApi.answer)
    return SparkApi.answer
