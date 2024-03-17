from  moudles.common_funcation import *
class gy_f_m_o:
    def __init__(self,sessionKey,bot_qq):
        # message_head = '>>>>接收到来自[好友]%s的消息:' % ( friend_name)
        self.sessionKey = sessionKey
        self.bot_qq=bot_qq

    def read_data(self,data):
        friend_name = data['subject']['nickname']
        name = data['subject']['nickname']#好友昵称
        remark = data['subject']['remark']#好友备注
        QQ = data['subject']['id']  # QQ就是好友的QQ啦
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
                        if m["text"]=="加入队伍":
                            try:
                                team_members=read_data("data/卖卡状态系统.json")["队伍成员"]
                                add_list("data/卖卡状态系统.json","队伍成员",int(QQ),sessionKey,"f")
                                message_chain = [{"type": "Plain", "text": str(QQ)+'加入队伍成功'
                                                                           }]
                                sendmeassage_friend(int(QQ),message_chain,sessionKey)
                            except:
                                print("bug大大的有")
                    elif n_type == 'Image':
                        message += '[图片:' + m['url'] + ']'
                    elif n_type == 'FlashImage':
                        message += '[闪照:' + m['url'] + ']'
                        url=m["url"]
                        qqqq=str(QQ)
                        # 3.13更新闪照模块
                    elif n_type == 'Voice':
                        message += '[语音消息(暂不支持读取）]'
                    elif n_type == 'Source':
                        message += ''
                    else:
                        print("未解析消息类型：" + n_type)

