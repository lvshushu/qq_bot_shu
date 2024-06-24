import random
import  threading
from moudles.common_funcation import *
class GuessNumber:
    def __init__(self,sessionKey,qq_bot):
        self.number_range=[]
        self.sessionKey=sessionKey
        self.bot_qq=qq_bot
        self.guess_group_list=[]
        self.target_num={}


    def main_function(self,data):
        self.guess_group_list=read_data("data/games/guess.json")["group_guess_list"]
        # /fetchLatestMessage?sessionKey=YourSessionKey&count=10
        self.guess_group(data)

    def guess_group(self,data):
        self.guess_group_list=read_data("data/games/guess.json")["group_guess_list"]
        try:
            group_qq = data[0]['sender']['group']['id']
            senderid = data[0]['sender']['id']  # 发送人的qq号
        except:
            group_qq = int(data[0]['subject']['id'])  # 群号
            senderid = self.bot_qq  # 发送人的qq号

        if int(group_qq) in self.guess_group_list:
            try:
                target_num = self.target_num[str(group_qq)]
                print(target_num)
            except:
                self.target_num[str(group_qq)]=self.get_target_num(group_qq)
                print(self.target_num)
            for m_type, value in data[0].items():
                if m_type == 'messageChain':  # 开始读取message_chain
                    for m in value:
                        n_type = m['type']
                        if n_type == 'At':
                            qq = m["target"]
                        elif n_type == 'Plain':
                            message= m['text']
                            message=message.replace(" ","")
            try:
                if int(qq)==self.bot_qq:
                    try:
                        if message=="不猜了":
                            self.guess_group_list.remove(group_qq)#游戏结束的标志
                            remove_list("data/games/guess.json","group_guess_list",group_qq,
                                        self.sessionKey,"f")
                            try:
                                target_guess=str(self.target_num[str(group_qq)])
                            except:
                                target_guess=500
                            message_chain_guess = [{"type": "At", "target": senderid},
                                                   {"type": "Plain", "text": " 好吧，正确答案是"+
                                                   str(target_guess)+",下次再来找鼠鼠玩吧"}]
                            try:
                                del self.target_num[str(group_qq)]
                            except Exception as e:
                                print(e)
                            sendmeassage_group(group_qq,message_chain_guess,self.sessionKey)
                            mmmm=""
                        try:
                            message=int(message)
                        except:
                            pass

                        if message==self.target_num[str(group_qq)]:
                            self.guess_group_list.remove(group_qq)#游戏结束的标志
                            del self.target_num[str(group_qq)]
                            remove_list("data/games/guess.json","group_guess_list",group_qq,
                                        self.sessionKey,"f")
                            message_chain_guess = [{"type": "At", "target": senderid},
                                                   {"type": "Plain", "text": " 恭喜你!猜对啦！下次再来找鼠鼠玩哦！"}]
                            sendmeassage_group(group_qq, message_chain_guess, self.sessionKey)
                        elif message<self.target_num[str(group_qq)]:
                            message_chain_guess = [{"type": "At", "target": senderid},
                                                   {"type": "Plain", "text": " 太小啦!"}]
                            sendmeassage_group(group_qq, message_chain_guess, self.sessionKey)
                        else:
                            message_chain_guess = [{"type": "At", "target": senderid},
                                                   {"type": "Plain", "text": " 太大啦!"}]
                            sendmeassage_group(group_qq, message_chain_guess, self.sessionKey)
                    except Exception as e:
                        print(e)
            except:
                erro_log("群聊猜数字函数出错")

    def get_target_num(self,group_qq):
        target_num=random.randint(1,1000)
        sendmeassage_friend(self.bot_qq, message_chain_make("群聊"+str(group_qq)+"答案是"+str(target_num)),self.sessionKey)
        return target_num



