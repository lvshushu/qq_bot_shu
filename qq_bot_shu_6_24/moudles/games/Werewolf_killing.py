import threading
from moudles.chuoyichuo import *
class Were_wolfkilling:
    def __init__(self,sessionKey,data):
        self.sessionKey=sessionKey
        self.group_on_game=[]
        self.group_ready=[]#缓冲区
        self.member_in_game = {
            "group_id": {
                "模式": "标局-6人",
                "所需人数": 6,
                "members":
                    [
                        2320864323,
                    ]
            }
        }
        self.data=data

    def function_to_run(self,sessionKey):
        self.group_message_back(sessionKey)
        print("在新线程中执行")

    def create_new_thread(self):
        thread = threading.Thread(target=self.function_to_run,args=(self.sessionKey))
        thread.start()

    def group_message_back(self,sessionKey):#这个地方本来可以写点模块化的东西的，但是我懒癌发作了，算了吧
        if self.data[0]["type"]=="GroupMessage":
            data=self.data[0]
            sessionKey = self.sessionKey
            message_chain = []
            self.group_list = read_data("data/group/group_zhaungtai.json")["基础功能"]
            member_name = data['sender']['memberName']  # 发送人的群昵称
            group_name = data['sender']['group']['name']  # 群聊名字
            group_qq = int(data['sender']['group']['id'])  # 群号
            senderid = data['sender']['id']  # 发送人的qq号
            #先写游戏未开始的准备部分，不打算做@模块，算是一个bug吧，不打算修的bug
            #算了还是先写
            message=""
            try:
                for m_type, value in data.items():
                    if m_type == 'messageChain':  # 开始读取message_chain
                        for m in value:
                            n_type = m['type']
                            if n_type == 'At':
                                message += '@somebody(人家还没做好啦）'  # 这个地方明天记得debug一下
                                qq = m["target"]
                            elif n_type == 'Plain':
                                panduan_text= m['text']
                                text_list=cut_string(panduan_text)
                            else:
                                print("未解析消息类型：" + n_type)
                        # print(message_head+message)
            except Exception as e:
                erro_log("debug2，狼人杀模块get_message_back函数出了问题"+str(e))#debug一下
                # 防撤回代码块放在这里，以后可能会用得到



