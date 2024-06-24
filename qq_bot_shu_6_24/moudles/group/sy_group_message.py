#先将所有类型的消息都放到这里，后面再重构
import moudles.others.chat_bot as chat_bot
from moudles.chuoyichuo import *
import moudles.others.chat_cat_girl as chat_cat_girl

import 测试.py代码 as py代码
import 测试.a as a
class g_m_o:
    def __init__(self,bot_qq,sessionKey):
        self.sessionKey=sessionKey
        self.bot_qq=bot_qq
        self.group_list=read_data("data/group/group_zhaungtai.json")["基础功能"]
        self.group_zhuangtai=read_data("data/group/group_zhaungtai.json")
        self.gif_to_apng=[]
        self.At=0


    def group_response_operate(self,data,sessionKey):
        sessionKey=self.sessionKey
        message_chain=[]
        self.group_list=read_data("data/group/group_zhaungtai.json")["基础功能"]
        member_name = "疯鼠"
        group_name = data['subject']['name']#群聊名字
        group_qq = int(data['subject']['id'])#群号
        senderid=self.bot_qq#发送人的qq号
        message=""
        try:#此处为不添加功能时可使用的指令，安全起见，菜单不在其中
            for m_type, value in data.items():
                if m_type == 'messageChain':  # 开始读取message_chain
                    for m in value:
                        n_type = m['type']
                        if n_type == 'Plain':
                            if m["text"] == "添加群聊":
                                file = "data/group/group_zhaungtai.json"
                                add_list(file, "基础功能", group_qq, sessionKey,"g")
                            elif m["text"] == "移除群聊":
                                file = "data/group/group_zhaungtai.json"
                                remove_list(file, "基础功能", group_qq, sessionKey,"g")
                            elif m["text"] == "开启戳一戳自动回复":
                                file = "data/group/group_zhaungtai.json"
                                add_list(file, "戳一戳自动回复", group_qq, sessionKey,"g")
                            elif m["text"] == "关闭戳一戳自动回复":
                                file = "data/group/group_zhaungtai.json"
                                remove_list(file, "戳一戳自动回复", group_qq, sessionKey,"g")
                            elif m["text"]=="获取群聊信息":
                                try:
                                    get_group_member_list(int(group_qq),sessionKey)
                                except:
                                    print(2)
                            elif m["text"] == "转格式":
                                self.gif_to_apng.append(senderid)
                                message_chain_3 = [
                                    {"type": "Plain", "text": "请发送gif图片，将自动为您转化成apng格式"}]
                                sendmeassage_group(group_qq, message_chain_3, sessionKey)
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
                                    self.At=m["target"]
                                    pass
                                elif n_type=='AtAll':
                                    message+='@全体成员  '
                                elif n_type=='Face':
                                    message+='[表情:'+m['name']+']'
                                elif n_type=='Plain':
                                    message+=m['text']
                                elif n_type == 'Image' :
                                    message += '[图片:' + m['url'] + ']'
                                    if senderid in self.gif_to_apng:
                                        try:
                                            gif_file = "imgs\\" + str(senderid) + ".gif"
                                            save_image(m["url"], gif_file)
                                            out_png_folder = "imgs\\" + str(senderid)
                                            py代码.gif_to_png_frames(gif_file, out_png_folder)
                                            a.aaaaaa("imgs/" + str(senderid))
                                            url = get_bendi_img_url(out_png_folder + "/out_put_apng.png", sessionKey)
                                            message_chain = [{'type': 'Image', "url": url}]
                                            self.gif_to_apng.remove(senderid)
                                        except Exception as e:
                                            message_chain_4 = [{"type": "Plain", "text": '出错啦，请联系管理员'}]
                                            sendmeassage_group(group_qq, message_chain_4, sessionKey)
                                            self.gif_to_apng.remove(senderid)
                                            print("debug3", e)
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
        except Exception as e:
            print("错误",e)
        if msg!="":
            message_chain=[{"type": "Plain", "text": ' '+msg},]
        if message_chain!=[]:
            sendmeassage_group(group_qq,message_chain,sessionKey)

    def chat_moudle(self,message,qq_group,sessionKey,qqtarget):
        msg_list=cut_string(message)
        if msg_list[0]=="ai问答":
            anwser = chat_bot.ai_bot_message_back(msg_list[1])
            message_chain = [{"type": "At", "target": int(qqtarget), "display": "@Mirai"},
                             {"type": "Plain", "text": ' ' + anwser},]
            sendmeassage_group(qq_group,message_chain,sessionKey)
        elif msg_list[0]=="猫娘":
            anwser = chat_cat_girl.ai_bot_message_back(msg_list[1])
            message_chain = [{"type": "At", "target": int(qqtarget), "display": "@Mirai"},
                             {"type": "Plain", "text": ' ' + anwser},]
            sendmeassage_group(qq_group,message_chain,sessionKey)
        elif msg_list[0]==" 禁言" or msg_list[0]==" 禁言":
            print(111)
            shut_up(qq_group,self.At,sessionKey,msg_list[1])
        self.At=0
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