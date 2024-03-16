import requests
import re
from settings import Settings
from P图 import picture_synthesis
import time
import json
class Group_operate:
    def __init__(self):
        self.name='None'
        self.Settings=Settings()
        with open("data\\players.json", "r", encoding="utf-8") as f:
            self.players = json.load(f)

    def lock_group_id(self,group_qq,qq,lock_target,sessionKey):#这个函数用来锁定群聊中某人的群昵称
        for key,value in lock_target.items():
            if int(key)==int(group_qq):
                for key_in,value_in in value.items():
                    if int(key_in)==int(qq):
                        new_name=value_in
                        target=int(group_qq)
                        qq=int(qq)
                        url = "http://localhost:8080/memberInfo"
                        xiugai={
                            "sessionKey": sessionKey,
                            "target": target,
                            "memberId": qq,
                            "info": {
                                "name": new_name
                            }
                        }
                        res = requests.post(url, json=xiugai)
    def xiugai_group_id(self,group_qq,qq,new_name,sessionKey):
        target=int(group_qq)
        qq=int(qq)
        url = "http://localhost:8080/memberInfo"
        xiugai={
            "sessionKey": sessionKey,
            "target": group_qq,
            "memberId": qq,
            "info": {
                "name": new_name
            }
        }
        res = requests.post(url, json=xiugai)


    def get_info(self,qq,sessionKey):#用这个函数来获取朋友的信息，之前使用这个来获取头像的，现在好像有点看不懂了？
        qq_sender = int(qq)
        url = "http://localhost:8080/userProfile"
        url='http://q.qlogo.cn/g?b=qq&nk=2320864323&s=640'
        send_q = {
            "sessionKey": sessionKey,
            "target": int(qq_sender),
        }
        response = requests.get(url, params=send_q)
        friend_infor = response.json()
        return friend_infor



    def sendmeassage_group(self, group_qq, qq, msg, text, target_text,sessionKey):
        if re.search(target_text, text):
            if  target_text=="MALE":
                if not re.search('FEMALE',text):
                    target = int(group_qq)
                    qq = int(qq)
                    url = "http://localhost:8080/sendGroupMessage"
                    send_message = {
                        "sessionKey": sessionKey,
                        "target": int(target),
                        "messageChain": [
                            {"type": "At", "target": qq, "display": "@Mirai"},
                            {"type": "Plain", "text": ' ' + msg},
                        ]
                    }
                    res = requests.post(url, json=send_message)
            else:
                target = int(group_qq)
                qq = int(qq)
                url = "http://localhost:8080/sendGroupMessage"
                send_message = {
                    "sessionKey": sessionKey,
                    "target": int(target),
                    "messageChain": [
                        {"type": "At", "target": qq, "display": "@Mirai"},
                        {"type": "Plain", "text": ' ' + msg},
                    ]
                }
                res = requests.post(url, json=send_message)

    def new_sendmeassage_group(self,group_qq,send_message_data,sessionKey):#没改好有bug
        url = "http://localhost:8080/sendGroupMessage"
        send_message = {
            "sessionKey": sessionKey,
            "target": int(group_qq),
            "messageChain": send_message_data}
        res = requests.post(url, json=send_message_data)
    def chuo(self,qq_target,group_target,sessionKey):
        url = "http://localhost:8080/sendNudge"
        send_message = {

            "sessionKey": sessionKey,
            "target": qq_target,
            'subject':group_target,
            'kind': 'Group'
        }
        res = requests.post(url, json=send_message)

    def Alice(self,group,sessionKey):
        url = "http://localhost:8080/sendGroupMessage"
        send_message = {
            "sessionKey": sessionKey,
            "target": int(group),
            "messageChain": [{"type": "Plain", "text": '邦邦咔邦，爱丽丝闪亮登场，勇者啊，呼唤爱丽丝，有什么事吗'},
                             {"type": "Image","url": "http://c2cpicdw.qpic.cn/offpic_new/2320864323//2320864323-3877207822-81FA7B792A63BD5CAAFFDD9D031604CB/0?term=2&is_origin=0"}

            ]
        }
        res = requests.post(url, json=send_message)

    def send_img(self,group,sessionKey,url_2):
        url = "http://localhost:8080/sendGroupMessage"
        send_message = {
            "sessionKey": sessionKey,
            "target": int(group),
            "messageChain": [{"type": "Image","url": url_2}
            ]
        }
        res = requests.post(url, json=send_message)


    def bianshengning(self,group,qq_sender,sessionKey):
        url = "http://q.qlogo.cn/g?b=qq&nk="+str(qq_sender)+"&s=640"
        response = requests.get(url)
        with open('0.jpg', 'wb') as f:
            f.write(response.content)
        picture_synthesis('1.jpg','0.jpg','result.jpg')
        url_1 = "http://localhost:8080/uploadImage"
        with open('result.jpg', "rb") as image:
            files = {"img": ('result.jpg', image)}
            send_msda={
                "sessionKey": sessionKey,
                "type": "friend"
            }# 添加其他需要发送的数据
            response = requests.post(url_1, data=send_msda,files=files)
        response=response.json()
        url_2=response['url']
        self.send_img(group,sessionKey,url_2)

    def bianshenghu(self,group,qq_sender,sessionKey):
        url = "http://q.qlogo.cn/g?b=qq&nk="+str(qq_sender)+"&s=640"
        response = requests.get(url)
        with open('0.jpg', 'wb') as f:
            f.write(response.content)
        picture_synthesis('3.jpg','0.jpg','result.jpg',None,1054,300)
        url_1 = "http://localhost:8080/uploadImage"
        with open('result.jpg', "rb") as image:
            files = {"img": ('result.jpg', image)}
            send_msda={
                "sessionKey": sessionKey,
                "type": "friend"
            }# 添加其他需要发送的数据
            response = requests.post(url_1, data=send_msda,files=files)
        response=response.json()
        url_2=response['url']
        self.send_img(group,sessionKey,url_2)

    def random_jpg(self,group,sessionKey):
        url = "https://api.52vmy.cn/api/img/tu/girl"
        response = requests.get(url)
        data = response.json()
        url_3 = data['url']
        response = requests.get(url_3)
        response = response.content
        with open("群聊\\suijitu.jpg", "wb") as f:
            f.write(response)
        url_1 = "http://localhost:8080/uploadImage"
        with open("群聊\\suijitu.jpg", "rb") as image:
            files = {"img": ('suijitu.jpg', image)}
            send_msda={
                "sessionKey": sessionKey,
                "type": "friend"
            }# 添加其他需要发送的数据
            response = requests.post(url_1, data=send_msda,files=files)
        response=response.json()
        url_2=response['url']
        self.send_img(group,sessionKey,url_2)

    def random_shuaige_jpg(self,group,sessionKey):
        url = "https://api.52vmy.cn/api/img/tu/boy"
        params = {
            "type": "JSON"
        }

        response = requests.get(url, params=params)
        data = response.json()
        url_3=data['url']
        response = response.content
        with open("群聊\\suijitu.jpg", "wb") as f:
            f.write(response)
        url_1 = "http://localhost:8080/uploadImage"
        with open("群聊\\suijitu.jpg", "rb") as image:
            files = {"img": ('result.jpg', image)}
            send_msda = {
                "sessionKey": sessionKey,
                "type": "friend"
            }  # 添加其他需要发送的数据
            response = requests.post(url_1, data=send_msda, files=files)
        response = response.json()
        url_2 = response['url']
        self.send_img(group, sessionKey, url_2)

    def search_jpg_360(self,group,sessionKey,text):
        response = requests.get(f'https://api.52vmy.cn/api/img/360?msg={text}')
        response=response.json()
        print(response)
        url_3=response['data']['url']
        response = requests.get(url_3)
        response = response.content
        with open("群聊\\suijitu.jpg", "wb") as f:
            f.write(response)
        url_1 = "http://localhost:8080/uploadImage"
        with open("群聊\\suijitu.jpg", "rb") as image:
            files = {"img": ('result.jpg', image)}
            send_msda = {
                "sessionKey": sessionKey,
                "type": "friend"
            }  # 添加其他需要发送的数据
            response = requests.post(url_1, data=send_msda, files=files)
        response = response.json()
        url_2 = response['url']
        self.send_img(group, sessionKey, url_2)


    def fa_feng(self,name,qq_group,sessionKey):
        '''
        url = "https://api.lolimi.cn/API/fabing/fb.php"
        params = {
            "name": " "+name+" "
        }

        response = requests.get(url, params=params)
        data = response.json()["data"]
        url = "http://localhost:8080/sendGroupMessage"
        send_message = {
            "sessionKey": sessionKey,
            "target": int(qq_group),
            "messageChain": [{"type": "Plain", "text": data},

                             ]
        }
        res = requests.post(url, json=send_message)
        mas_ID=res.json()['messageId']
        print('删除中')
        time.sleep(30)
        send_message = {
            "sessionKey": sessionKey,
            "target": int(qq_group),
            "messageId": mas_ID
        }
        print(send_message)
        res = requests.post(url='http://localhost:8080/recall', json=send_message)
        print(res.json())'''
        url = "http://localhost:8080/sendGroupMessage"
        send_message = {
            "sessionKey": sessionKey,
            "target": int(qq_group),
            "messageChain": [{"type": "Plain", "text": '该功能已禁用'}
                             ]
        }
        res = requests.post(url, json=send_message)


    def chuo_all(self,qq_group,sessionKey):
        url = "http://localhost:8080/memberList?sessionKey=" + str(sessionKey) + "&target=" + str(qq_group)
        res=requests.get(url)
        response=res.json()
        print(response)
        qq_list=[]
        for qq_target in response["data"]:
            qq=qq_target['id']
            qq_list.append(qq)
        次数=0
        for qq_target in qq_list:
            if 次数<=20:
                次数+=1
                self.chuo(qq_target,qq_group,sessionKey)













