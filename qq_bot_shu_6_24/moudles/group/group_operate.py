#先将所有类型的消息都放到这里，后面再重构
import moudles.others.chat_bot as chat_bot
from  moudles.common_funcation import *
import moudles.others.chat_cat_girl as chat_cat_girl
import 测试.py代码 as py代码
import 测试.a as a
class m_o:
    def __init__(self,bot_qq,sessionKey):
        self.sessionKey=sessionKey
        self.bot_qq=bot_qq
        self.group_list=read_data("data/group/group_zhaungtai.json")["基础功能"]
        self.group_zhuangtai=read_data("data/group/group_zhaungtai.json")
        self.gif_to_apng=[]


    def group_response_operate(self,data,sessionKey):
        sessionKey=self.sessionKey
        message_chain=[]
        self.group_list=read_data("data/group/group_zhaungtai.json")["基础功能"]
        member_name = data['sender']['memberName']#发送人的群昵称
        group_name = data['sender']['group']['name']#群聊名字
        group_qq = int(data['sender']['group']['id'])#群号
        senderid=data['sender']['id']#发送人的qq号
        message=""
        try:#此处为不添加功能时可使用的指令，安全起见，菜单不在其中
            for m_type, value in data.items():
                if m_type == 'messageChain':  # 开始读取message_chain
                    for m in value:
                        n_type = m['type']
                        if n_type == 'Plain':
                            if m["text"]=="添加群聊":
                                file="data/group/group_zhaungtai.json"
                                add_list(file,"基础功能",group_qq,sessionKey,"g")
                            elif m["text"]=="移除群聊":
                                file="data/group/group_zhaungtai.json"
                                remove_list(file,"基础功能",group_qq,sessionKey,"g")
                            elif m["text"]=="开启戳一戳自动回复":
                                file = "data/group/group_zhaungtai.json"
                                add_list(file, "戳一戳自动回复", group_qq, sessionKey,"g")
                            elif m["text"]=="关闭戳一戳自动回复":
                                file="data/group/group_zhaungtai.json"
                                remove_list(file,"戳一戳自动回复",group_qq,sessionKey,"g")
                            elif m["text"]=="转格式":
                                self.gif_to_apng.append(senderid)
                                message_chain_3=[{"type":"Plain","text":"请发送gif图片，将自动为您转化成apng格式"}]
                                sendmeassage_group(group_qq,message_chain_3,sessionKey)
        except:
            pass
        self.group_list=read_data("data/group/group_zhaungtai.json")["基础功能"]
        if int(group_qq) in self.group_list:
                try:
                    for m_type,value in data.items():
                        if m_type=='messageChain':#开始读取message_chain
                            for m in value:
                                n_type=m['type']
                                if n_type=='Quote':
                                    message+=str(m['senderId'])+'的消息被引用了：'
                                elif n_type=='At':
                                    message+='@somebody(人家还没做好啦）'#这个地方明天记得debug一下
                                    qq=m["target"]
                                elif n_type=='AtAll':
                                    message+='@全体成员  '
                                elif n_type=='Face':
                                    message+='[表情:'+m['name']+']'
                                elif n_type=='Plain':
                                    message+=m['text']
                                elif n_type=='Image' or n_type=='FlashImage':
                                    message+='[图片:'+m['url']+']'
                                    if senderid in self.gif_to_apng:
                                        try:
                                            gif_file="imgs\\"+str(senderid)+".gif"
                                            save_image(m["url"],gif_file)
                                            out_png_folder="imgs\\"+str(senderid)
                                            py代码.gif_to_png_frames(gif_file,out_png_folder)
                                            a.aaaaaa("imgs/"+str(senderid))
                                            url=get_bendi_img_url(out_png_folder+"/out_put_apng.png",sessionKey)
                                            message_chain=[{'type': 'Image',"url":url}]
                                            self.gif_to_apng.remove(senderid)
                                        except Exception as e:
                                            message_chain_4=[{"type": "Plain", "text": '出错啦，请联系管理员'}]
                                            sendmeassage_group(group_qq,message_chain_4,sessionKey)
                                            self.gif_to_apng.remove(senderid)
                                            print("debug3",e)

                                elif n_type=='FlashImage':
                                    message+='[闪照:'+m['url']+']'
                                elif n_type=='Voice':
                                    message+='[语音消息:'+m['url']+']'
                                elif n_type == 'Source':#看不懂这是啥了
                                    message += ''
                                else:
                                    print("未解析消息类型："+n_type)
                            #print(message_head+message)
                except Exception as e:
                    print('debug1')#这个地方的bug有着非常特殊的提示
                    #防撤回代码块放在这里，以后可能会用得到
                    '''
                        message_id = data[0]["messageChain"][0]["id"]#从这一行开始都是为了防撤回
                    message_time = data[0]["messageChain"][0]["time"]
                    try:
                        self.Settings.message_recall["Friend"][QQ][str(message_id)] = [message_time, remark]
                    except Exception as e:
                        self.Settings.message_recall["Friend"][QQ] = {}
                        self.Settings.message_recall["Friend"][QQ][str(message_id)] = [message_time, remark]'''
        msg=self.menu_response(message)
        try:
            self.chat_moudle(message,group_qq,sessionKey,senderid)
        except:
            print("错误")
        if msg!="":
            message_chain=[{"type": "Plain", "text": ' '+msg}]
        if message_chain!=[]:
            sendmeassage_group(group_qq,message_chain,sessionKey)
    def sendmeassage_group(self, group_qq,qq,message_chain,sessionKey):
        target = int(group_qq)
        #qq = int(qq)
        url = "http://localhost:8080/sendGroupMessage"
        send_message = {
            "sessionKey": sessionKey,
            "target": int(target),
            "messageChain":message_chain
                #[{"type": "At", "target": qq, "display": "@Mirai"},{"type": "Plain", "text": ' 你好'},]
                #message_chain是一个列表，以上是一个示例
        }
        res = requests.post(url, json=send_message)


    def menu_response(self,text):#菜单及回复###这个地方完全可以改成读取json键值对的形式,这个地方的回复是不考虑图片的
        back_text=''
        try:
            self.menu=read_data("data/group/menu_operate")["菜单"]
            for m in self.menu:
                t=m["text"]
                b=m["back_text"]
                if t==text:
                    back_text=b[:]
            return back_text
        except Exception as e:
            print(e)

    def chat_moudle(self,message,qq_group,sessionKey,qqtarget):
        msg_list=cut_string(message)
        if msg_list[0]=="ai问答":
            anwser = chat_bot.ai_bot_message_back(msg_list[1])
            message_chain = [{"type": "At", "target": int(qqtarget), "display": "@Mirai"},
                             {"type": "Plain", "text": ' ' + anwser},]
            sendmeassage_group(qq_group,message_chain,sessionKey)
        elif msg_list[0]=="猫娘":
            print(1)
            anwser = chat_cat_girl.ai_bot_message_back(msg_list[1])
            print(anwser)
            message_chain = [{"type": "At", "target": int(qqtarget), "display": "@Mirai"},
                             {"type": "Plain", "text": ' ' + anwser},]
            sendmeassage_group(qq_group,message_chain,sessionKey)
        elif msg_list[0] == "执行代码":
            pass
            code = ""
            for i in range(2, len(msg_list)):
                if i == len(msg_list) - 1:
                    code += str(msg_list[i])
                else:
                    code += str(msg_list[i]) + "."
            lang = msg_list[1]

    def read_group_au_list(self,authority_name):#这个函数应该会被弃用
        try:
            list_target=read_data("data/group/group_zhaungtai.json")[authority_name]
            return list_target
        except:
            print('报错啦')
            return []

    def add_list(self,file,list_name,target_qq,sessionKey):
        self.group_list = read_data(file)[list_name]
        zong = read_data(file)
        if int(target_qq) not in self.group_list:
            self.group_list.append(int(target_qq))
            zong[list_name] = self.group_list
            save_data(zong, file)
            message_chain_1 = [{"type": "Plain", "text": '添加%s成功'%list_name}, ]
        else:
            message_chain_1 = [{"type": "Plain", "text": '添加失败，该群已开启%s'%list_name}, ]
        sendmeassage_group(target_qq, message_chain_1, sessionKey)
    def remove_list(self,file,list_name,target_qq,sessionKey):
        self.group_list = read_data(file)[list_name]
        zong = read_data(file)
        if int(target_qq) in self.group_list:
            self.group_list.remove(int(target_qq))
            zong[list_name] = self.group_list
            save_data(zong, file)
            message_chain_1 = [{"type": "Plain", "text": '移除%s成功'%list_name}, ]
        else:
            message_chain_1 = [{"type": "Plain", "text": '移除失败，该群未开启%s'%list_name}, ]
        sendmeassage_group(target_qq, message_chain_1, sessionKey)
    def listen_message_group(self,data):#对群消息进行回应
        pass
