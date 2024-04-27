import requests
from moudles.common_funcation import *
def remove_shut_up(group_qq,target_qq,sessionKey):
        qq = int(target_qq)
        url = "http://localhost:8080/unmute"
        try:
            shut = {
                "sessionKey": sessionKey,
                "target": group_qq,
                "memberId": qq
            }
            res = requests.post(url, json=shut)
        except:
            pass
def group_meber_name(group_qq,sessionKey,target_qq,group_name):#来来来
    url = "http://localhost:8080/memberInfo"
    try:
        dict = {
            "sessionKey": sessionKey,
            "target": int(group_qq),
            "memberId": int(target_qq),
            "info": {
                "name": group_name,
            }
        }
        res = requests.post(url, json=dict)
        print(res.json())
        if res.json()["msg"]=="success":
            message_chain=message_chain_make("更改群名片成功")
            sendmeassage_group(group_qq,message_chain,sessionKey)
            pass

    except:
        pass

def send_wav(group_qq,file,sessionKey):
    url="http://localhost:8080/uploadVoice"
    with open(file, "rb") as voice:
        files = {"voice": (file, voice)}
        dict = {
            "sessionKey": sessionKey,
            "type":"group",
        }
        res = requests.post(url, data=dict, files=files)
        print(res.json())
        voice_ID = res.json()["voiceId"]
    try:
        url="http://localhost:8080/sendGroupMessage"
        dict = {
            "sessionKey": sessionKey,
            "target": int(group_qq),
            "messageChain": [{
                "type": "Voice",
                "voiceId": voice_ID
            }]
        }
        print(2)
        res = requests.post(url, json=dict)
        print(res.json())

    except:
        pass

