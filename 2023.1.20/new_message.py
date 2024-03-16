#在1.10的更新中，所有戳一戳相关代码移至此处
import time
import traceback


from  settings import Settings
from group_operate import Group_operate
from  friend_operate import Friend_operate
from games import Games
import json
import chat_bot
import random
import requests


def cut_string(s):#这个函数用来分隔各项参数,想的是能不能分隔多个（应该能，就是索引不太好搞，也不太确定用户体验怎么样）
    #return s.split('.', 1)[-1]#以后用点来分隔了
    return s.split('.')#以后用点来分隔了，直接返回一个列表
class New_message:
    def __init__(self):
        self.zahanweifu=None#占个位置
        self.Games=Games()
        self.Settings=Settings()
        self.Groupt=Group_operate()
        self.Friend_operate=Friend_operate()
        self.bot_qq=2320864323#这个地方使用你的bot的qq号
        self.zhuren=123456#改为号主，这里的账号拥有最高权限
        self.administer=json.load(open("data\\administers.json","r",encoding="utf-8"))[1]#这个列表中的账号拥有仅次于主人的权限
        self.users=[]#这个列表中的账号拥有普通权限（高于一般用户）
        self.group_open_or_not=self.Settings.group_open_or_not


    def sava_data(self,information_json,file):#这个函数用来存储信息
        with open(file, "w", encoding="utf-8") as f: json.dump(information_json, f,
                                                                               ensure_ascii=False, indent=4)

    def read_data(self,data,sessionKey):
        if data[0]['type']=='GroupMessage':
            member_name = data[0]['sender']['memberName']
            group_name = data[0]['sender']['group']['name']
            group_qq = data[0]['sender']['group']['id']
            senderid=data[0]['sender']['id']
            message_head='>>>>接收到来自群聊[%s]的%s的消息:'%(group_name,member_name)
            message=""
            if group_name == '壮壮捡漏集团318':#这里其实是冗余代码，以后以此为基础将要屏蔽的群组加入其中
                pass
            else:#读取消息
                try:
                    for m_type,value in data[0].items():
                        if m_type=='messageChain':
                            for m in value:
                                n_type=m['type']
                                if n_type=='Quote':
                                    message+=str(m['senderId'])+'的消息被引用了：'
                                elif n_type=='At':
                                    message+='@somebody(人家还没做好啦）'
                                    qq=m["target"]
                                elif n_type=='AtAll':
                                    message+='@全体成员\t'

                                elif n_type=='Face':
                                    message+='[表情:'+m['name']+']'
                                elif n_type=='Plain':
                                    message+=m['text']
                                    if '请使用新版手机QQ查收红包' in message:
                                        self.Groupt.sendmeassage_group(group_qq, 2228489853, "来抢红包", '', '', sessionKey)
                                    elif int(senderid) in self.administer:#这里用来存储管理员可执行的操作
                                        if "禁言" in message:
                                            time_shut = cut_string(message)[-1]
                                            try:
                                                time_shut = int(time_shut)
                                                url = "http://localhost:8080/mute"
                                                shut = {
                                                    "sessionKey": sessionKey,
                                                    "target": group_qq,
                                                    "memberId": int(qq),
                                                    "time": time_shut
                                                }
                                                res = requests.post(url, json=shut)
                                            except:
                                                pass
                                elif n_type=='Image' or n_type=='FlashImage':
                                    message+='[图片:'+m['url']+']'
                                elif n_type=='FlashImage':
                                    message+='[闪照:'+m['url']+']'
                                elif n_type=='Voice':
                                    message+='[语音消息:'+m['url']+']'
                                elif n_type == 'Source':
                                    message += ''
                                else:
                                    message += '[文件]'
                            message+='\n'
                            #print(message_head+message)
                except Exception as e:
                    print('读取消息时出了bug')#这个地方的bug有着非常特殊的提示
                try:
                    if str(group_qq) in self.Settings.message_recall["Group"].keys():
                        message_id = data[0]["messageChain"][0]["id"]
                        sender_name=data[0]["sender"]["memberName"]
                        qq_sender=data[0]["sender"]["id"]
                        self.Settings.message_recall["Group"][str(group_qq)][str(message_id)] = [qq_sender,sender_name
                                                                                                 ,group_name,message]
                        self.sava_data(self.Settings.message_recall, "data/message_recall.json")
                        #这个地方我是打算在每次重启之后进行清楚的哈，不然有点太占用资源了
                except Exception  as e:
                    print("照常理来书评不会出bug的",e)
                    '''
                        message_id = data[0]["messageChain"][0]["id"]#从这一行开始都是为了防撤回
                    message_time = data[0]["messageChain"][0]["time"]
                    try:
                        self.Settings.message_recall["Friend"][QQ][str(message_id)] = [message_time, remark]
                    except Exception as e:
                        self.Settings.message_recall["Friend"][QQ] = {}
                        self.Settings.message_recall["Friend"][QQ][str(message_id)] = [message_time, remark]'''
        elif data[0]['type']=="GroupRecallEvent":
            try:
                group_qq=data[0]["group"]["id"]
                message_id = data[0]["messageId"]
                info=self.Settings.message_recall["Group"][str(group_qq)][str(message_id)]
                if str(group_qq) in self.Settings.message_recall["Group"].keys():
                    self.Friend_operate.sendmeassage_friend(self.bot_qq,f"检测到有人撤回群消息啦\n来自群聊：{info[2]} 群号：{group_qq}"
                                                                        f"\n发送人：{info[1]}\n消息内容：{info[3]}",'',
                                                            '',sessionKey)
            except Exception as e:
                print(e,"出错啦")


        elif data[0]['type'] == 'GroupSyncMessage':
            member_name = '旅鼠'
            group_name = data[0]['subject']['name']
            group_qq = data[0]['subject']['id']
            # message='>>>>接收到来自群聊[%s]的%s的消息:'%(group_name,member_name)
            message = ""
            try:
                for m_type, value in data[0].items():
                    if m_type == 'messageChain':
                        for m in value:
                            n_type = m['type']
                            if n_type == 'Quote':
                                message += str(m['senderId']) + '的消息被引用了：'
                            elif n_type == 'At':
                                # message+='@somebody(人家还没做好啦）'
                                qq_target = m["target"]
                            elif n_type == 'AtAll':
                                message += '@全体成员\t'
                            elif n_type == 'Face':
                                message += '[表情:' + m['name'] + ']'
                            elif n_type == 'Plain':
                                message += m['text']
                                try:
                                    if '禁言' in message:
                                        time_shut = cut_string(message)[-1]
                                        try:
                                            time_shut = int(time_shut)
                                            url = "http://localhost:8080/mute"
                                            shut = {
                                                "sessionKey": sessionKey,
                                                "target": group_qq,
                                                "memberId": qq_target,
                                                "time": time_shut
                                            }
                                            res = requests.post(url, json=shut)
                                        except:
                                            pass

                                    elif m['text'] == '添加防撤回':
                                        self.Settings.message_recall["Group"][str(group_qq)] = {}
                                        self.Groupt.sendmeassage_group(group_qq, self.bot_qq, "添加成功", '', '',
                                                                      sessionKey)
                                        self.sava_data(self.Settings.message_recall, 'data\\message_recall.json')
                                    elif m['text'] == '取消防撤回':
                                        del self.Settings.message_recall['Group'][str(group_qq)]
                                        self.Groupt.sendmeassage_group(group_qq, self.bot_qq, "取消成功", '', '',
                                                                       sessionKey)
                                        self.sava_data(self.Settings.message_recall, 'data\\message_recall.json')
                                except Exception as e:
                                    print(e)
                            elif n_type == 'Image' or n_type == 'FlashImage':
                                message += '[图片:' + m['url'] + ']'
                            elif n_type == 'FlashImage':
                                message += '[闪照:' + m['url'] + ']'
                            elif n_type == 'Voice':
                                message += '[语音:' + m['url'] + ']'
                                self.Friend_operate.sendmeassage_friend(self.bot_qq,message,"","",sessionKey)
                            elif n_type == 'Source':
                                message += ''
                            else:
                                message += '[文件]'

                        message += '\n'

                        # print(message)这个版本不再显示消息
            except Exception as e:
                print(e,type)
                print('读取消息时出了bug')
        elif data[0]['type'] == 'FriendMessage':
            friend_name =data[0]['sender']['nickname']
            name = data[0]['sender']['nickname']
            remark = data[0]['sender']['remark']
            QQ = data[0]['sender']['id']#QQ就是好友的QQ啦
            #message_head = '>>>>接收到来自[好友]%s的消息:' % ( friend_name)
            message=''
            try:
                for m_type, value in data[0].items():
                    if m_type == 'messageChain':
                        message_id = data[0]["messageChain"][0]["id"]#从这一行开始都是为了防撤回
                        message_time = data[0]["messageChain"][0]["time"]
                        try:
                            self.Settings.message_recall["Friend"][QQ][str(message_id)] = [message_time, remark]
                        except Exception as e:
                            self.Settings.message_recall["Friend"][QQ] = {}
                            self.Settings.message_recall["Friend"][QQ][str(message_id)] = [message_time, remark]
                        for message_id, message_info in self.Settings.message_recall["Friend"][QQ].copy().items():
                            time_now = time.time()
                            if time_now - int(message_info[0]) >= 120:
                                del self.Settings.message_recall["Friend"][QQ][message_id]#到这一行结束
                        for m in value:
                            n_type = m['type']
                            if n_type == 'Quote':
                                message += str(m['senderId']) + '的消息被引用了：'
                            #elif n_type == 'At':
                                #Friend_message哪来的At消息
                                #message += '@somebody(人家还没做好啦）'
                            #elif n_type == 'AtAll':我是煞笔
                                #message += '@全体成员\t'
                            elif n_type == 'Face':
                                message += '[表情:' + m['name'] + ']'#大多数时候是没有name的，这个应该是mirai本身的bug
                            elif n_type == 'Plain':
                                message += m['text']
                                if message=="你好":
                                    self.Friend_operate.sendmeassage_friend(self.bot_qq,"你好","","",sessionKey)
                            elif n_type == 'Image' :
                                message += '[图片:' + m['url'] + ']'
                            elif n_type == 'FlashImage':
                                message += '[闪照:' + m['url'] + ']'
                                self.Friend_operate.sendmeassage_friend(self.bot_qq,f"检测到有人发送闪照啦！\n发送者:{remark}\t发送者qq号:{QQ}\n"+message,"","",sessionKey)
                                #1.31更新闪照模块
                            elif n_type == 'Voice':
                                message += '[语音消息(暂不支持读取）]'
                            elif n_type == 'Source':
                                message += ''
                            else:
                                message += '[文件(暂不支持读取）]'
                        self.Settings.message_recall["Friend"][QQ][str(message_id)].append(message)
                        try:
                            result = cut_string(message)[-1]
                        except:
                            pass
                        if int(QQ) == 2025773217 or int(QQ) == 2120792939:#黑名单功能做出来之前先把这两行保留，免得妹妹生气
                            pass
                        elif message == '猜数字':
                            self.Games.start_game_friend(QQ, sessionKey)
                        elif message == '康康美女':
                            self.Friend_operate.random_jpg(QQ, sessionKey)
                        elif 'ai问答' in message:
                            anwser = chat_bot.ai_bot_message_back(result)
                            self.Friend_operate.sendmeassage_friend(QQ, anwser, '', '', sessionKey)
                        elif self.Games.guess_number_friend:#当猜数字游戏已经开始时，执行以下代码
                            self.Games.cai_friend(QQ, message, sessionKey)
                        elif '自动回复' in message:
                            guanjianci=cut_string(message)[-2]
                            try:
                                self.Settings.ato_response_Friend[str(QQ)][guanjianci]=result#迫不及待了，现在就试试
                            except:
                                self.Settings.ato_response_Friend[str(QQ)]={}
                                self.Settings.ato_response_Friend[str(QQ)][guanjianci] = result
                            self.sava_data(self.Settings.ato_response_Friend,"data/ato_response_Friend.json")

                        #这是最容易出bug的部分，明天起床后先在本地跑一跑吧
                        try:
                            try:
                                ato_response=self.Settings.ato_response_Friend[str(QQ)]#先try一下有没有将这个qq存进去
                            except:
                                self.Settings.ato_response_Friend[str(QQ)]={}
                                ato_response=self.Settings.ato_response_Friend[str(QQ)]
                            for key, value in ato_response.items():  # 自动回复,给它做成好友定制吧，然后发个说说汇报一下进度
                                self.Friend_operate.sendmeassage_friend(QQ, value, message, key, sessionKey)
                        except Exception as e:
                            print('好友定制关键词回复功能出bug了，你确定你不看看吗？')
                            print(e)
                        message += '\n'
                        #print(message_head+message)在这一版本中，不再在终端或者控制台中显示消息以节约内存资源
            except Exception as e:
                print(e)
                traceback.print_exc()
                print('读取消息时出了bug')
        elif data[0]['type']=='FriendSyMessage':
            pass
        elif data[0]['type']== 'NudgeEvent':#这个地方的用来制作自动回戳，以及其他的有关戳一戳的事件
            try:
                target_qq = data[0]['fromId']
                target_qq = int(target_qq)
                kind = data[0]['subject']['kind']
                panduan = data[0]['target']
                if target_qq == self.bot_qq:  # 要给别人用的话这里记得改成bot_qq（已经改了嗷，我真是好人
                    pass
                    #print('>>>>你戳了一下自己\n')
                elif kind == 'Friend':  # 这个地方有bug，记得改
                    print('>>>>好友戳一戳\n')  # 这个地方有bug，记得改
                    self.Friend_operate.chuo(target_qq,sessionKey)  # 这个地方有bug，记得改
                elif kind == 'Group' and panduan == self.bot_qq:  # 这个地方有bug，记得改
                    print('>>>>群聊戳一戳')  # 这个地方有bug，记得改
                    target_group = data[0]['subject']['id']  # 这个地方有bug，记得改
                    target_group = int(target_group)  # 这个地方有bug，记得改
                    if str(target_qq)=="2228489853":
                        choices=[""]
                        choice=random.choice(choices)
                        self.Groupt.sendmeassage_group(target_group, target_qq,choice,"","",sessionKey)
                        self.Groupt.chuo(target_qq, target_group, sessionKey)
                    elif str(target_qq)=="1944001329":
                        choices = ["\n这是个帅哥","\n这是个暖男","\n小姐姐们加爆他"]
                        choice=random.choice(choices)
                        self.Groupt.sendmeassage_group(target_group, target_qq,choice,"","",sessionKey)
                        self.Groupt.chuo(target_qq, target_group, sessionKey)
                    else:
                        choices=["\n给钱了吗就拍我？没钱别碰你鼠哥尾巴。","\n还拍？警告过你了嗷，鼠哥的牙齿可不是摆设！","\n鼠哥白了你一眼你自己体会","\n(面露凶光）你给钱没？！"]
                        choice=random.choice(choices)
                        self.Groupt.sendmeassage_group(target_group,target_qq,choice,"","",sessionKey)
                        self.Groupt.chuo(target_qq, target_group, sessionKey)  # 这个地方有bug，记得改,说实话，我已经忘了bug是啥了
                else:
                    pass
            except Exception as e:
                traceback.print_exc()
        elif data[0]['type']== 'MemberJoinEvent':
            try:
                qq_target=int(data[0]['member']['id'])
                qq_group=int(data[0]['member']['group']['id'])
                for traget_group,ato_response in self.Settings.ato_geoup_welcome_new_member.items():
                    if str(qq_group)==traget_group:
                        self.Groupt.sendmeassage_group(qq_group,qq_target,ato_response,' ',' ',sessionKey)
                        break
            except Exception as e:
                print(e)
        elif data[0]['type']=="FriendRecallEvent":
            try:
                QQ=data[0]["authorId"]
                message_id=data[0]["messageId"]
                message_recall_real=self.Settings.message_recall["Friend"][QQ][str(message_id)]
                self.Friend_operate.sendmeassage_friend(self.bot_qq,"检测到有人撤回消息啦\n"+'撤回者：'+message_recall_real[-2]
                                                        +"\n消息内容:"+message_recall_real[-1],'','',sessionKey)
            except Exception as e:
                print(e)
                traceback.print_exc()






    def break_jai_1(self,group_qq,sessionKey,data):
        try:
            m = data[0]['messageChain'][1:]
            if str(group_qq) not in self.Settings.last_news.keys():
                try:
                    self.Settings.last_news.update({str(group_qq):m})
                except Exception as e:
                    print(e)
            else:
                try:
                    if m==self.Settings.last_news[str(group_qq)]:
                        self.Settings.last_news.update({str(group_qq): 'fsdfsdsdffxc'})
                        #self.Groupt.break_jia1(group_qq,sessionKey)
                    else:
                        self.Settings.last_news.update({str(group_qq): m})
                except Exception as e:
                    print(e)
                    traceback.print_exc()
        except:
            print('出bug了')

        pass

    def open_ato_reponse(self,group_qq):
        try:#没做好的，等我去groupopert里写个函数再回来
            if self.Settings.group_settings["自动回复"][group_qq][1]=="True":
                self.Settings.group_settings["自动回复"][group_qq][1]="True"
        except:
            pass



