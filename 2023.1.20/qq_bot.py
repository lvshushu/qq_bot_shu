#这个版本旨在解决一些优化问题包括但不限于：保存无效照片、防加一功能的不完善、无法对指定群聊开启或关闭一些功能
#在本地json文件中对群聊私聊关键词进行处理，而不是每次重启后就消失
#清楚对应账号的使用功能的权限，关闭对应账号群聊的所有功能
#删除冗余代码
#本次更新自1.10始
#预计1.16结束
#中间可能会在logs文件中加入10个左右文件夹
#开干————1.10
#更新日志1.13 3:04 增加了自己diy自动回复的功能，让自动回复更加的灵活，睡觉
import asyncio
import http.client
import json
import threading
import re
import requests
import chat_bot

from group_operate import Group_operate
from friend_operate import Friend_operate
from settings import Settings
from games import Games
from new_message import New_message
import os
from moudles import creat_sessionKey
'''
script_path = "C:\\Users\\23208\\Desktop\\mcl - 快捷方式.lnk"

os.system(f'start cmd /k "{script_path}"')
time.sleep(5)
'''

class bot:
    def __init__(self):

        self.bot_qq = 2320864323 # 这里输入bot的qq号
        self.Info=creat_sessionKey.Info_informession()
        self.VisitHttpPath = self.Info.VisitHttpPath
        self.verifyKey = self.Info.verifyKey
        self.sessionKey = self.Info.sessionKey
        self.bot_qq = self.Info.bot_qq  # 这里记得在creat_sessionKey文件中更改qq_bot为你的机器人qq
        self.settings = Settings()
        self.Group_operate = Group_operate()
        self.Friend_operate = Friend_operate()
        self.Games = Games()
        self.New_message = New_message()


    def bind(self):
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

    async def message(self):
        # /fetchLatestMessage?sessionKey=YourSessionKey&count=10
        VisitHttpPath = self.VisitHttpPath
        sessionKey = self.sessionKey
        while True:
            try:
                VisitHttpPath.request(method='GET', url='/fetchLatestMessage?sessionKey=' + sessionKey + '&count=10')
                response = VisitHttpPath.getresponse().read().decode("utf-8")
                data = json.loads(response)
                if data['data'] != []:
                    threading.Thread(target=self.dispose, args=(data,)).start()
            except Exception as e:
                print(e)

    def dispose(self, data):
        ato_reponse_group = self.settings.ato_reponse_group
        ato_response_Friend = self.settings.ato_response_Friend
        sessionKey = self.sessionKey
        try:
            data = data['data']
            type = str(data[0]['type'])
            try:
                self.New_message.read_data(data,sessionKey)
            except Exception as e:
                print(e)

            if type == 'GroupSyncMessage':
                try:
                    if data[0]['messageChain'][1]['type'] == 'At' and data[0]['messageChain'][2]['type'] == 'Plain':
                        text = data[0]['messageChain'][2]['text']
                        target_qq = data[0]['messageChain'][1]['target']
                        text = data[0]['messageChain'][2]['text']
                        qq_group = data[0]['subject']['id']

                        def cut_string(s):
                            return s.split('，', 1)[-1]

                        result = cut_string(text)
                        if '修改群昵称' in text:
                            self.Group_operate.xiugai_group_id(qq_group, target_qq, result, sessionKey)
                            self.Group_operate.sendmeassage_group(qq_group, target_qq, ' 已经改了你的群昵称啦', ' ',
                                                                  ' ', sessionKey)
                        #elif '禁言' in text:
                            #qq_target = data[0]['messageChain'][1]['target']
                            #qq_sender = data[0]['sender']['id']
                            #qq_group = data[0]['sender']['group']['id']
                            #self.Games.shut_up(qq_group, qq_target,qq_sender, sessionKey)
                            #功能禁用

                    if data[0]['messageChain'][1]['type'] == 'Plain':
                        text = data[0]['messageChain'][1]['text']
                        qq_group = data[0]['subject']['id']
                        if text=="chuoall":
                            self.Group_operate.chuo_all(qq_group,sessionKey)





                except Exception as e:
                    print(e)
            elif type == 'GroupMessage':
                try:
                    qq_sender = data[0]['sender']['id']
                    qq_group = data[0]['sender']['group']['id']

                    if int(qq_sender) == 2025773217 or int(qq_sender) == 2120792939:
                        pass
                    else:
                        try:
                            self.Group_operate.lock_group_id(qq_group, qq_sender, self.settings.group_lock_id,
                                                             sessionKey)
                        except Exception as e:
                            print(e)
                        if data[0]['messageChain'][1]['type'] == 'At' and data[0]['messageChain'][2]['type'] == 'Plain':
                            qq_sender = data[0]['sender']['id']
                            qq_target = data[0]['messageChain'][1]['target']
                            text = data[0]['messageChain'][2]['text']
                            qq_group = data[0]['sender']['group']['id']
                            member_name = data[0]['sender']['memberName']
                            group_name = data[0]['sender']['group']['name']

                            def cut_string(s):
                                return s.split('，', 1)[-1]
                            result = cut_string(text)
                            if '修改群昵称' in text:
                                self.Group_operate.xiugai_group_id(qq_group, qq_target, result, sessionKey)
                                self.Group_operate.sendmeassage_group(qq_group, qq_target, ' 已经改了你的群昵称啦', ' ',
                                                                      ' ', sessionKey)
                            elif '锁定群昵称' in text:
                                new = {str(qq_group): {str(qq_target): result}}
                                self.settings.group_lock_id.update(new)
                                self.Group_operate.xiugai_group_id(qq_group, qq_target, result, sessionKey)
                                self.Group_operate.sendmeassage_group(qq_group, qq_target, ' 已经锁定了你的群昵称啦',
                                                                      ' ', ' ', sessionKey)
                            elif '禁言' in text:
                                self.Games.shut_up(qq_group, qq_target,qq_sender,sessionKey)
                            elif 'ai问答' in text:
                                anwser = chat_bot.ai_bot_message_back(result)
                                self.Group_operate.sendmeassage_group(qq_group, qq_sender, '' + anwser, ' ', ' ',
                                                                      sessionKey)
                            elif '抢劫'in text:
                                self.Games.rob_player(qq_sender,qq_target,qq_group,sessionKey)
                                pass
                            if qq_target == self.bot_qq and text == ' 猜数字':
                                self.Games.start_game(qq_group, qq_sender, sessionKey)
                            elif qq_target==self.bot_qq and text==' 创建新角色':
                                self.Games.new_player(qq_sender,qq_group,sessionKey)
                            elif qq_target==self.bot_qq and text==' 我要工作':
                                self.Games.player_work(qq_sender,qq_group,sessionKey)
                            elif qq_target ==self.bot_qq and text==' 查看信息':
                                self.Games.view_player_datas(qq_sender, qq_group, sessionKey)
                            elif qq_target ==self.bot_qq and text==' 签到':
                                self.Games.qian_dao( qq_group,qq_sender, sessionKey)
                            elif qq_target ==self.bot_qq and ' 我要存款'in text:
                                result=result.replace(' ','')
                                self.Games.cun_money(qq_group,qq_sender,result,sessionKey)
                            elif qq_target ==self.bot_qq and ' 使用道具'in text:
                                result=result.replace(' ','')
                                self.Games.use_daoju(qq_sender,qq_group,result,sessionKey)
                            elif qq_target ==self.bot_qq and ' 我要取钱'in text:
                                result=result.replace(' ','')
                                self.Games.qu_money(qq_group,qq_sender,result,sessionKey)
                            elif ' 转账'in text:
                                pass
                                result=result.replace(' ','')
                                self.Games.zhuanzhang(qq_sender,qq_target,qq_group,result,sessionKey)
                            elif qq_target ==self.bot_qq and text==' 购买破旧的水果刀':
                                self.Games.buy_friut_knief(qq_sender, qq_group, sessionKey)
                            elif qq_target == self.bot_qq:
                                self.Games.cai(qq_group, qq_sender, text, sessionKey)
                        if data[0]['messageChain'][1]['type'] == 'Plain':
                            text = data[0]['messageChain'][1]['text']
                            member_name = data[0]['sender']['memberName']
                            group_name = data[0]['sender']['group']['name']
                            qq_sender = data[0]['sender']['id']
                            qq_group = data[0]['sender']['group']['id']
                            if group_name == '壮壮捡漏集团318':
                                pass
                            elif text == '爱丽丝':
                                qq_group = data[0]['sender']['group']['id']
                                self.Group_operate.Alice(qq_group, sessionKey)
                            elif text == '宁红夜':
                                self.Group_operate.bianshengning(qq_group,qq_sender,sessionKey)
                            elif text == '胡为':
                                self.Group_operate.bianshenghu(qq_group,qq_sender,sessionKey)
                            elif text=='康康美女':
                                self.Group_operate.random_jpg(qq_group,sessionKey)
                            elif text == '康康帅哥':
                                self.Group_operate.random_shuaige_jpg(qq_group, sessionKey)
                            elif text=='对我发疯':
                                self.Group_operate.fa_feng(member_name,qq_group,sessionKey)
                            elif '360搜图' in text:
                                msg=text.split(' ')[-1]
                                self.Group_operate.search_jpg_360(qq_group,sessionKey,msg)
                            else:
                                if re.search("晚安", text):
                                    qq_sender = int(qq_sender)
                                    url = "http://localhost:8080/userProfile"
                                    sessionKey = self.sessionKey
                                    send_q = {
                                        "sessionKey": sessionKey,
                                        "target": int(qq_sender),
                                    }
                                    response = requests.get(url, params=send_q)
                                    friend_infor = response.json()
                                    sex = friend_infor['sex']
                                    for key, value in ato_reponse_group.items():
                                        self.Group_operate.sendmeassage_group(qq_group, qq_sender, value, sex, key,
                                                                              sessionKey)
                                for key, value in ato_reponse_group.items():
                                    self.Group_operate.sendmeassage_group(qq_group, qq_sender, value, text, key,
                                                                          sessionKey)
                        elif data[0]['messageChain'][1]['type'] == 'Image':
                            member_name = data[0]['sender']['memberName']
                            group_name = data[0]['sender']['group']['name']
                            if group_name == '壮壮捡漏集团318':
                                pass
                            else:
                                url = data[0]['messageChain'][1]['url']
                                folder_name = "群聊"
                                file_name = str(data[0]['messageChain'][1]['imageId'])
                                headers = {
                                    'User-Agent': "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10"
                                }
                                img_data = requests.get(url).content
                                if not os.path.exists(folder_name):
                                    os.makedirs(folder_name)


                                with open(os.path.join(folder_name, file_name), "wb") as f:
                                    f.write(img_data)
                except Exception as e:  # 出现超级表情时会进入此界面
                    print(e)
        except Exception as e:
            pass


if __name__ == '__main__':
    b = bot()
    asyncio.run(b.run())
