#先将所有类型的消息都放到这里，后面再重构
import moudles.others.chat_bot as chat_bot
import subprocess
from  moudles.common_funcation import *
from moudles.group.common_function_group import *
import moudles.others.chat_cat_girl as chat_cat_girl
import 测试.py代码 as py代码
import 测试.a as a
from moudles.games.guess_number import GuessNumber
import threading
class m_o:
    def __init__(self,bot_qq,sessionKey):
        self.sessionKey=sessionKey
        self.bot_qq=bot_qq
        self.group_list=read_data("data/group/group_zhaungtai.json")["基础功能"]
        self.group_zhuangtai=read_data("data/group/group_zhaungtai.json")
        self.gif_to_apng=[]
        self.qq=0
        self.At=0
        self.suijitu=0


    def group_response_operate(self,data):
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
        except Exception as e:
            print(e)
            erro_log(e)
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
                                    #message+='@somebody(人家还没做好啦）'#这个地方明天记得debug一下
                                    self.At = m["target"]
                                    self.qq= m["target"]
                                elif n_type=='AtAll':
                                    message+='@全体成员  '
                                elif n_type=='Face':
                                    message+='[表情:'+m['name']+']'
                                elif n_type=='Plain':
                                    message+=m['text']
                                elif (n_type=='Image') or (n_type=='FlashImage'):
                                    #message+='[图片:'+m['url']+']'
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
                                elif n_type=='FlashImage':
                                    message+='[闪照:'+m['url']+']'
                                elif n_type=='Voice':
                                    message+='[语音消息:'+m['url']+']'
                                elif n_type == 'Source':#看不懂这是啥了
                                    message += ''
                                else:
                                    print("未解析消息类型："+n_type)
                    self.qq=0
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
            mes=cut_string(message)
            print(mes)
            self.image_back(group_qq,senderid,sessionKey,mes)
        except Exception as e:
            print("错误",e)
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
        list_guanli = read_data("config/basic_config.json")["管理员"]
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
        elif  msg_list[0]==" 禁言":
            try:
                list_guanli=read_data("config/basic_config.json")["管理员"]
            except:
                pass
            if int(qqtarget) in list_guanli:
                shut_up(qq_group,self.At,sessionKey,msg_list[1])
            else:
                message_chain = [{"type": "At", "target": int(qqtarget), "display": "@Mirai"},
                                 {"type": "Plain", "text": ' 你没有这个权限' }, ]
                sendmeassage_group(qq_group, message_chain, sessionKey)
        elif  msg_list[0]==" 解除禁言":
            try:
                list_guanli = read_data("config/basic_config.json")["管理员"]
            except:
                pass
            if int(qqtarget) in list_guanli:
                remove_shut_up(qq_group, self.At, sessionKey)
            else:
                message_chain = [{"type": "At", "target": int(qqtarget), "display": "@Mirai"},
                                 {"type": "Plain", "text": ' 你没有这个权限'}, ]
                sendmeassage_group(qq_group, message_chain, sessionKey)
        elif msg_list[0]=="猜数字":
            add_list("data/games/guess.json","group_guess_list",qq_group,sessionKey,"guess")
        elif msg_list[0]=="我要头衔":
            self.change_head_name(sessionKey,qq_group,int(qqtarget),msg_list[1])
        elif msg_list[0]=="我要玩狼人杀":
            send_wav(qq_group,"data\\wav\\wav\\天黑请闭眼.wav",sessionKey)
        elif msg_list[0]==" 群名片":
            print(self.bot_qq)
            if int(self.bot_qq)==int(self.At):
                message_chain_1 = [{"type": "Plain", "text": ' 别改老子群名片'}]
                sendmeassage_group(qq_group, message_chain_1, sessionKey)
                shut_up(qq_group,qqtarget,sessionKey,300)
            else:
                group_meber_name(qq_group, sessionKey, self.At, msg_list[1])
        elif int(qqtarget) in list_guanli:
            if msg_list[0] == "入群欢迎":
                try:
                    dict = read_data("data/group/atu_welcome_grop.json")
                    dict[str(qq_group)] = msg_list[1]
                    save_data(dict,"data/group/atu_welcome_grop.json")
                    mes_chain_wel = message_chain_make("入群欢迎制作成功")
                    sendmeassage_group(qq_group, mes_chain_wel, sessionKey)
                except Exception as e:
                    erro_log(str(e) + "入群欢迎出了问题")
        songs_dict=read_data("data/wav/songs.json")
        for key,value in songs_dict.items():#音频发送
            if msg_list[0]==key:
                send_wav(qq_group, value, sessionKey)
        #群聊自动回复
        try:
            for target_mes,back_text_chain in read_data("data/group/atu_group_response.json").items():
                if message==target_mes:
                    sendmeassage_group(qq_group,back_text_chain,sessionKey)
                pass
        except Exception as e:
            print(e)

        self.At=0

    def add_list(self,file,list_name,target_qq,sessionKey):###疑似冗余代码
        self.group_list = read_data(file)[list_name]
        zong = read_data(file)
        if int(target_qq) not in self.group_list:
            self.group_list.append(int(target_qq))
            zong[list_name] = self.group_list
            save_data(zong, file)
            message_chain_1 = [{"type": "Plain", "text": '添加%s成功'%list_name},]
        else:
            message_chain_1 = [{"type": "Plain", "text": '添加失败，该群已开启%s'%list_name}, ]
        sendmeassage_group(target_qq, message_chain_1, sessionKey)
    def remove_list(self,file,list_name,target_qq,sessionKey):#疑似冗余代码
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
    def change_head_name(self,sessionKey,group_qq,qq_target,head_name):
        print(111)
        url="http://localhost:8080/memberInfo"
        send_mes={
        "sessionKey":sessionKey,
        "target": int(group_qq),
        "memberId": int(qq_target),
        "info": {
            "specialTitle": head_name
        }
    }
        res=requests.post(url,json=send_mes)
        print(res.text)
        meschain=[{"type": "At", "target": int(qq_target), "display": "@Mirai"},
                             {"type": "Plain", "text": ' ' + "更改群头衔成功"}]
        sendmeassage_group(group_qq,meschain,sessionKey)
    def listen_message_group(self,data):#对群消息进行回应
        pass

    def image_back(self,qq_group,qq_target,sessionKey,target_text):
        dict=read_data("data/group/images_back")
        target_text=target_text[0]
        for name,url in dict.items():
            if target_text==name:
                try:

                    message_chain_back = [{"type": "At", "target": int(qq_target), "display": "@Mirai"},
                                              {"type": "Plain", "text": ' ' + "稍等哦，正在为你准备图片"},
                                           ]
                    sendmeassage_group(qq_group,message_chain_back,sessionKey)
                    response = requests.get(url)
                    response = response.content
                    try:
                        format=get_image_format(response)

                    except:
                        print("出错啦")
                    print(format)
                    print(type(format))
                    try:
                        self.suijitu+=1
                        self.suijituname="suijitu"+str(self.suijitu)+"."+format
                        try:
                            delete_file("data\\群聊\\"+self.suijituname)
                        except:
                            pass
                        with open("data\\群聊\\"+self.suijituname, "wb") as f:
                            f.write(response)
                        url_1 = "http://localhost:8080/uploadImage"
                    except Exception as e:
                        print(e)
                        print(4313)
                    if format == "WEBP":
                        try:
                            file="data\\群聊\\suijitu"+str(self.suijitu)+".JPEG"
                            delete_file(file)#大概率是冗余代码，我应该在发送之后删除
                        except Exception as e:
                            print(e,7684532)
                        try:

                            cmd = f"cd D:\\23208\\qq_bot_shu"
                        except Exception as e:
                            print(e)
                            print(1241)
                        subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                        cmd = '.\\ffmpeg -i ' + "data\\群聊\\" + self.suijituname + " data\\群聊\\suijitu"+str(self.suijitu)+".JPEG"
                        self.suijituname = "suijitu" + str(self.suijitu) + ".JPEG"
                        # 使用subprocess.run()执行命令
                        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                text=True)
                        format = "JPEG"
                        print("stdout:", result.stdout)
                        print("stderr:", result.stderr)
                    try:
                        print(233,self.suijituname)
                        with open("data\\群聊\\"+self.suijituname, "rb") as image:
                            files = {"img": (self.suijituname, image)}
                            send_msda = {
                                "sessionKey": sessionKey,
                                "type": "friend"
                            }  # 添加其他需要发送的数据
                            response = requests.post(url_1, data=send_msda, files=files)
                    except Exception as e:
                        print(e)
                        print(312)
                    response = response.json()
                    print(response)
                    url_2 = response['url']
                    message_chain_img_back = [{"type": "At", "target": int(qq_target), "display": "@Mirai"},
                                              {"type": "Plain", "text": ' ' + "这是你要的图"},
                                              {"type": "Image", "url": url_2}]
                    sendmeassage_group(qq_group,message_chain_img_back,sessionKey)
                except Exception as e:
                    print(e)#特别 的冗余代码，希望别人能帮我优化

    def shut_up(group_qq, qq, sessionKey, t):  # 不完善，没有正确的回馈消息
        qq = int(qq)
        url = "http://localhost:8080/mute"
        try:
            shut = {
                "sessionKey": sessionKey,
                "target": group_qq,
                "memberId": qq,
                "time": int(t)
            }
            res = requests.post(url, json=shut)
        except:
            pass


