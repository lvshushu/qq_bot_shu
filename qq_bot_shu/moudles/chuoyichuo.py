from moudles.common_funcation import *
import random
class chuo:
    def __init__(self,data,sessionKey,bot_qq):
        self.target_qq = int(data['fromId'])
        self.kind = data['subject']['kind']
        self.panduan = data['target']
        self.sessionKey=sessionKey
        self.data=data
        self.bot_qq=bot_qq
        self.group_zhuangtai=read_data("data/group/group_zhaungtai.json")
    def Nudegeback(self):
        try:
            sessionKey=self.sessionKey
            kind=self.kind
            panduan=self.panduan
            if self.target_qq == self.bot_qq:  # 要给别人用的话这里记得改成bot_qq（已经改了嗷，我真是好人
                pass
                #print('>>>>你戳了一下自己\n')
            elif kind == 'Friend':  # 这个地方有bug，记得改
                pass
                #self.Friend_operate.chuo(self.target_qq,sessionKey)  # 这个地方有bug，记得改
            elif kind == 'Group' and panduan == self.bot_qq:  # 这个地方有bug，记得改
                self.group_zhuangtai=read_data("data/group/group_zhaungtai.json")
                chuo_list = self.group_zhuangtai["戳一戳自动回复"]
                chuo_back_list=self.group_zhuangtai["戳一戳自动回戳"]
                target_group = self.data['subject']['id']  # 这个地方有bug，记得改
                target_group = int(target_group)  # 这个地方有bug，记得改
                if int(target_group) in chuo_list:
                    if str(self.target_qq)=="1944001329":
                        choices = ["\n这是个帅哥","\n这是个暖男","\n小姐姐们加爆他"]
                        choice=random.choice(choices)
                        message_chain=[{"type": "At", "target": self.target_qq, "display": "@Mirai"},
                                       {"type": "Plain", "text": ' ' + choice}]
                        sendmeassage_group(target_group,message_chain,sessionKey)
                    else:
                        choices=["\n给钱了吗就拍我？没钱别碰你鼠哥尾巴。","\n还拍？警告过你了嗷，鼠哥的牙齿可不是摆设！",
                                 "\n鼠哥白了你一眼你自己体会","\n(面露凶光）你给钱没？！",
                                 "\nv我5块定制专属戳一戳回复"]
                        choice=random.choice(choices)
                        message_chain=[{"type": "At", "target": self.target_qq, "display": "@Mirai"},
                                       {"type": "Plain", "text": ' ' + choice}]
                        sendmeassage_group(target_group,message_chain,sessionKey)
                if int(target_group) in chuo_back_list:
                    chuo_group(int(panduan),int(target_group),sessionKey)
        except Exception as e:
            print(e)