#这是qq_bot_mouse的重构版本，旨在使代码更易懂，更好修改
#想新加的功能目前只有功能菜单
import asyncio
import http.client
import json
import threading
from moudles.group.group_operate import m_o
from moudles.group.sy_group_message import g_m_o
from moudles.chuoyichuo import chuo
from moudles.friend.friend_operate import f_m_o
from moudles.friend.sy_friend_operate import gy_f_m_o
from moudles.common_funcation import *

'''
script_path = "C:\\Users\\23208\\Desktop\\mcl - 快捷方式.lnk"

os.system(f'start cmd /k "{script_path}"')
time.sleep(5)
'''

class bot:
    def __init__(self, host="localhost", port=8080):
        self.info=json.load(open("config/basic_config.json", 'r', encoding='utf-8'))
        self.bot_qq = self.info["bot_qq"] # 这里输入bot的qq号
        self.VisitHttpPath = http.client.HTTPConnection(host, port)
        self.verifyKey="Wuhao118744"
        self.sessionKey = self.bind()#这里用来创建全局使用的sessionKey
        self.g_m_o=m_o(self.bot_qq,self.sessionKey)
        self.gy_m_o=g_m_o(self.bot_qq,self.sessionKey)
        self.f_m_o=f_m_o(self.sessionKey,self.bot_qq)
        self.gy_f_m_o=gy_f_m_o(self.sessionKey,self.bot_qq)


    def bind(self):#这个函数用来创建全局使用的sessionKey
        print('该程序由wh制作')
        auto = json.dumps({"verifyKey": self.verifyKey})
        VisitHttpPath = self.VisitHttpPath
        VisitHttpPath.request("POST", "/verify", auto)
        response = VisitHttpPath.getresponse()
        session = response.read().decode("utf-8")
        print("主人，恭喜您认证成功啦:" + str(session))

        sessionKey = json.loads(session)['session']
        bind = json.dumps({"sessionKey": sessionKey, "qq":self.bot_qq })  # 此处输入bot的qq号
        VisitHttpPath.request("POST", '/bind', bind)
        response = VisitHttpPath.getresponse().read().decode("utf-8")
        print("主人，恭喜你绑定成功啦:" + str(response))
        return sessionKey

    async def run(self):
        method = [asyncio.create_task(self.message())]
        await asyncio.gather(*method)

    async def message(self):#这个函数用来接受消息
        #/fetchLatestMessage?sessionKey=YourSessionKey&count=10
        VisitHttpPath = self.VisitHttpPath
        sessionKey = self.sessionKey
        while True:
            try:
                VisitHttpPath.request(method='GET', url='/fetchLatestMessage?sessionKey=' + sessionKey + '&count=10')
                response = VisitHttpPath.getresponse().read().decode("utf-8")
                data = json.loads(response)
                if data['data'] != []:
                    threading.Thread(target=self.dispose, args=(data,)).start()#在这个函数中用来执行模块
            except Exception as e:
                print(e)

    def dispose(self, data):
        sessionKey = self.sessionKey#sessionKey只赋值一次就够了
        try:
            data = data['data']
            print(data)#测试阶段用，正式版去掉这一行
            if data[0]["type"]=="GroupMessage":
                data=data[0]
                self.g_m_o.group_response_operate(data,self.sessionKey)
            if data[0]["type"]=="GroupSyncMessage":
                data=data[0]
                self.gy_m_o.group_response_operate(data,self.sessionKey)
            elif data[0]["type"]=="NudgeEvent":
                data=data[0]
                chuo_back=chuo(data,self.sessionKey,self.bot_qq)
                try:
                    chuo_back.Nudegeback()
                except Exception as e:
                    print(e)
            elif data[0]["type"]=="FriendMessage":
                data=data[0]
                self.f_m_o.readdata(data)
            elif data[0]["type"]=="FriendSyncMessage":
                data=data[0]
                self.gy_f_m_o.read_data(data)

        except Exception as e:
            pass

if __name__ == '__main__':
    b = bot()
    asyncio.run(b.run())
