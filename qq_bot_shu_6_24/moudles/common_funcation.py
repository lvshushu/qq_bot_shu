import json
import requests
import time
import os
def save_data(information_json, file):  # 这个函数用来存储信息
    with open(file, "w", encoding="utf-8") as f: json.dump(information_json, f,
                                                           ensure_ascii=False, indent=4)



def read_data( file):  # 这个函数用来读取信息
    data = json.load(open(file, 'r', encoding='utf-8'))
    return data

def cut_string(s):#这个函数用来分隔各项参数,想的是能不能分隔多个（应该能，就是索引不太好搞，也不太确定用户体验怎么样）
    #return s.split('.', 1)[-1]#以后用点来分隔了
    return s.split('.')#以后用点来分隔了，直接返回一个列表

def get_img_url(file):#将已知路径的本地图片上传mirai服务器并返回图片url
    pass#这个地方应该要返回图片的url


def sendmeassage_group( group_qq,message_chain,sessionKey):
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

def sendmeassage_friend(qq,message_chain,sessionKey):
    target=int(qq)
    url = "http://localhost:8080/sendFriendMessage"
    send_message = {
        "sessionKey": sessionKey,
        "target": target,
    "messageChain": message_chain
    }
    res = requests.post(url, json=send_message)

def chuo_group(qq_target,group_target,sessionKey):
    url = "http://localhost:8080/sendNudge"
    send_message = {

        "sessionKey": sessionKey,
        "target": qq_target,
        'subject':group_target,
        'kind': 'Group'
    }
    res = requests.post(url, json=send_message)
def add_list(file,list_name,target_qq,sessionKey,g_o_f):
    group_list = read_data(file)[list_name]
    zong = read_data(file)
    if int(target_qq) not in group_list:
        group_list.append(int(target_qq))
        zong[list_name] = group_list
        save_data(zong, file)
        message_chain_1 = [{"type": "Plain", "text": '添加%s成功'%list_name}, ]
    else:
        message_chain_1 = [{"type": "Plain", "text": '添加失败，该群已开启%s'%list_name}, ]
    if g_o_f=="g":
        try:
            sendmeassage_group(target_qq, message_chain_1, sessionKey)
        except:
            pass
def remove_list(file,list_name,target_qq,sessionKey,g_o_f):
    group_list = read_data(file)[list_name]
    zong = read_data(file)
    if int(target_qq) in group_list:
        group_list.remove(int(target_qq))
        zong[list_name] = group_list
        save_data(zong, file)
        message_chain_1 = [{"type": "Plain", "text": '移除%s成功'%list_name}, ]
    else:
        message_chain_1 = [{"type": "Plain", "text": '移除失败，该群未开启%s'%list_name}, ]
    if g_o_f=="g":
        try:
            sendmeassage_group(target_qq, message_chain_1, sessionKey)
        except:
            pass


def get_info(qq, sessionKey):  # 用这个函数来获取朋友的信息，之前使用这个来获取头像的，现在好像有点看不懂了？
    qq_sender = int(qq)
    url = "http://localhost:8080/userProfile"
    send_q = {
        "sessionKey": sessionKey,
        "target": int(qq_sender),
    }
    response = requests.get(url, params=send_q)
    friend_infor = response.json()
    print(friend_infor)
    return friend_infor

def get_time():
    # 获取当前时间戳
    timestamp = time.time()
    # 将时间戳转换为本地时间
    local_time = time.localtime(timestamp)
    # 将本地时间格式化为年月日时
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return formatted_time

def get_group_member_list(group_qq,sessionKey):
    #memberList?sessionKey=YourSessionKey&target=123456789
    url="http://localhost:8080/memberList"
    send_q = {
        "sessionKey": sessionKey,
        "target": group_qq
    }
    response = requests.get(url,params=send_q)
    group_infor = response.json()
    print(group_infor)#打印成员信息以后可能会有用
    member_list=[]
    member_info=[]
    try:
        for dictionary in group_infor["data"]:
            member_info.append({"昵称":
                                    dictionary["memberName"],
                                "id":dictionary["id"]
                                })
            member_list.append(dictionary["id"])
        #message_chain_1 = [{"type": "Plain", "text":"群成员信息如下：\n"+member_info}]
        #sendmeassage_group(group_qq,message_chain_1,sessionKey)
    except Exception as e:
        member_info=[]
        print(e)
    print(member_info,member_list,sep="\n")
    return member_list,member_info
def erro_log(errotext):
    with open("logs/errors_log.txt", "a", encoding="utf-8") as f:#报错日志
        time=get_time()
        f.write(time+"  "+errotext)

def save_image(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"图片已成功保存到 {file_path}")
    except Exception as e:
        print(f"保存图片时出错： {e}")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"文件 {file_path} 已被成功删除。")
    except FileNotFoundError:
        print(f"文件 {file_path} 不存在。")
    except Exception as e:
        print(f"删除文件 {file_path} 时出错： {e}")


def get_bendi_img_url(img_file,sessionKey):
    url_1 = "http://localhost:8080/uploadImage"
    with open(img_file, "rb") as image:
        files = {"img": (img_file, image)}
        send_msda={
            "sessionKey": sessionKey,
            "type": "friend"
        }# 添加其他需要发送的数据
        response = requests.post(url_1, data=send_msda,files=files)
    response=response.json()
    url_2=response['url']
    return url_2
def shut_up(group_qq,qq,sessionKey,t):#不完善，没有正确的回馈消息
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

