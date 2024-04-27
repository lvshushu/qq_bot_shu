from  moudles.common_funcation import *
class f_m_o:
    def __init__(self,sessionKey,bot_qq):
        # message_head = '>>>>接收到来自[好友]%s的消息:' % ( friend_name)
        self.sessionKey = sessionKey
        self.bot_qq=bot_qq

    def readdata(self,data):
        friend_name = data['sender']['nickname']
        name = data['sender']['nickname']#好友昵称
        remark = data['sender']['remark']#好友备注
        QQ = data['sender']['id']  # QQ就是好友的QQ啦
        message = ''
        sessionKey = self.sessionKey
        for m_type, value in data.items():
            if m_type == 'messageChain':
                """message_id = data["messageChain"][0]["id"]  # 从这一行开始都是为了防撤回
                message_time = data["messageChain"][0]["time"]
                try:
                    self.Settings.message_recall["Friend"][QQ][str(message_id)] = [message_time, remark]
                except Exception as e:
                    self.Settings.message_recall["Friend"][QQ] = {}
                    self.Settings.message_recall["Friend"][QQ][str(message_id)] = [message_time, remark]
                for message_id, message_info in self.Settings.message_recall["Friend"][QQ].copy().items():
                    time_now = time.time()
                    if time_now - int(message_info[0]) >= 120:
                        del self.Settings.message_recall["Friend"][QQ][message_id]  # 到这一行结束"""
                for m in value:
                    n_type = m['type']
                    if n_type == 'Quote':
                        message += str(m['senderId']) + '的消息被引用了：'
                    elif n_type == 'Face':
                        message += '[表情:' + m['name'] + ']'  # 大多数时候是没有name的，这个应该是mirai本身的bug
                    elif n_type == 'Plain':
                        message += m['text']
                        mes=m["text"]
                        panduan=cut_string(mes)
                        if message == "晚安":
                            #来个message_chain的模板
                            #message_chain = [{"type": "At", "target": int(qqtarget), "display": "@Mirai"},
                             #{"type": "Plain", "text": ' ' + anwser},]
                            message_chain=[{"type": "Plain", "text": '滚去睡觉'}]
                            sendmeassage_friend(int(QQ), message_chain, sessionKey)
                        elif panduan[0]=="联通":
                            self.liantong(panduan,QQ,sessionKey)
                        bake_text=self.liantong_menu_response(m["text"])
                        try:
                            message_chain=[{"type": "Plain", "text": bake_text}]
                            sendmeassage_friend(QQ,message_chain,sessionKey)
                        except Exception as e:
                            print(e)
                    elif n_type == 'Image':
                        message += '[图片:' + m['url'] + ']'
                    elif n_type == 'FlashImage':
                        message += '[闪照:' + m['url'] + ']'
                        url=m["url"]
                        qqqq=str(QQ)
                        message_chain = [{"type": "Plain", "text": '检测到有人发送闪照啦\n发送人：%s\n发送人qq：%s\n图片：'
                                                                   %(remark,qqqq)},
                            {"type": "Image","url": url}
                        ]
                        sendmeassage_friend(self.bot_qq,message_chain,sessionKey)
                        # 3.13更新闪照模块
                    elif n_type == 'Voice':
                        message += '[语音消息(暂不支持读取）]'
                    elif n_type == 'Source':
                        message += ''
                    else:
                        print("未解析消息类型：" + n_type)


    def liantong(self,panduan,QQ,sessionKey):
        if panduan[0] == "联通":
            member_list = read_data("data/卖卡状态系统.json")["队伍成员"]
            if int(QQ) in member_list:
                try:
                    panduan_1 = panduan[1]
                    if panduan_1 == "是否办卡":
                        target_qqq = int(panduan[2])
                        target_group = int(panduan[3])
                        add_list("data/卖卡状态系统.json", "已买卡", target_qqq, sessionKey,
                                 "f")
                    elif panduan_1 == "备注":
                        target_qqq = int(panduan[2])
                        add_note = panduan[3]
                        info = read_data("data/卖卡状态系统.json")
                        try:
                            text = "队员" + str(QQ) + "添加了如下备注\n" + add_note
                        except:
                            text = ""
                            # 这个地方要添加错误日志
                        try:
                            info["备注"][str(target_qqq)].append(text)
                        except:
                            info["备注"][str(target_qqq)] = []
                            info["备注"][str(target_qqq)].append(text)
                        save_data(info, "data/卖卡状态系统.json")
                        message_chain = [{"type": "Plain", "text": '添加备注成功'}]
                        sendmeassage_friend(int(QQ), message_chain, sessionKey)
                    elif panduan_1 == "查看信息":
                        target_qqq = int(panduan[2])
                        info = read_data("data/卖卡状态系统.json")
                        name_target = get_info(target_qqq, sessionKey)['nickname']
                        text = f"{name_target}的信息如下:\n"
                        for name, list in info.items():
                            if name == "备注":
                                pass
                            elif name == "队伍成员":
                                pass
                            else:
                                if target_qqq in list:
                                    text += name + "\n"
                        try:
                            list_2 = info["备注"][str(target_qqq)]
                        except:
                            info["备注"][str(target_qqq)] = []
                        for i in range(len(info["备注"][str(target_qqq)]) - 1, -1, -1):
                            text += info["备注"][str(target_qqq)][i] + "\n"
                        message_chain = [{"type": "Plain", "text": text}]
                        sendmeassage_friend(int(QQ), message_chain, sessionKey)
                    elif panduan_1 == "添加办卡":
                        info = read_data("data/卖卡状态系统.json")
                        target_qqq = int(panduan[2])
                        add_list("data/卖卡状态系统.json", "已买卡", target_qqq, sessionKey, "f")
                        message_chain = [{"type": "Plain", "text": "添加成功"}]
                        sendmeassage_friend(QQ, message_chain, sessionKey)
                    elif panduan_1 == "婉拒办卡":
                        info = read_data("data/卖卡状态系统.json")
                        target_qqq = int(panduan[2])
                        add_list("data/卖卡状态系统.json", "婉拒买卡", target_qqq, sessionKey, "f")
                        message_chain = [{"type": "Plain", "text": "添加成功"}]
                        sendmeassage_friend(QQ, message_chain, sessionKey)
                    elif panduan_1 == "不办卡":
                        info = read_data("data/卖卡状态系统.json")
                        target_qqq = int(panduan[2])
                        add_list("data/卖卡状态系统.json", "明确意向不买卡", target_qqq, sessionKey, "f")
                        message_chain = [{"type": "Plain", "text": "添加成功"}]
                        sendmeassage_friend(QQ, message_chain, sessionKey)
                except Exception as e:
                    print(e)
                    print("联通格式出错")
    def liantong_menu_response(self,text):#菜单及回复###这个地方完全可以改成读取json键值对的形式,这个地方的回复是不考虑图片的
        back_text=''
        try:
            self.menu=read_data("data/group/menu_operate")["联通菜单"]
            for m in self.menu:
                t=m["text"]
                b=m["back_text"]
                if t==text:
                    back_text=b[:]
            return back_text
        except Exception as e:
            print(e)




