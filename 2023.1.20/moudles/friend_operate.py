import requests
import re
class Friend_operate:
    def __init__(self):
        self.name='None'

    def sendmeassage_friend(self,qq,msg,text,target_text,sessionKey):
        if re.search(target_text, text):
            target=int(qq)
            url = "http://localhost:8080/sendFriendMessage"
            send_message = {
                "sessionKey": sessionKey,
                "target": target,
            "messageChain": [
                {"type": "Plain", "text": msg},
            ]
            }
            res = requests.post(url, json=send_message)

    def chuo(self,qq_target,sessionKey):
        url = "http://localhost:8080/sendNudge"
        send_message = {

            "sessionKey": sessionKey,
            "target": qq_target,
            'subject':qq_target,
            'kind': 'Friend'
        }
        res = requests.post(url, json=send_message)
        response=res.json()
        print(response)

    def random_jpg(self,qq,sessionKey):
        response = requests.get('https://api.yimian.xyz/img')
        response = response.content
        with open("群聊\\suijitu.jpg", "wb") as f:
            f.write(response)
        url_1 = "http://localhost:8080/uploadImage"
        with open("群聊\\suijitu.jpg", "rb") as image:
            files = {"img": ('result.jpg', image)}
            send_msda={
                "sessionKey": sessionKey,
                "type": "friend"
            }# 添加其他需要发送的数据
            response = requests.post(url_1, data=send_msda,files=files)
        response=response.json()
        url_2=response['url']
        target = int(qq)
        url = "http://localhost:8080/sendFriendMessage"
        send_message = {
            "sessionKey": sessionKey,
            "target": target,
            "messageChain": [{"type": "Image","url": url_2}
            ]
        }
        res = requests.post(url, json=send_message)