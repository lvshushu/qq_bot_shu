#这里用来存储所有小游戏
from settings import Settings
import random
import requests
import threading
import time
import json
from group_operate import Group_operate
class Games:
    def __init__(self):

        #游戏猜数字
        self.guess_number=False
        self.target_number=0
        self.guess_number_friend=False
        self.target_number_friend=0
        self.Group_operate=Group_operate()
        self.file_lock = threading.Lock()


        #游戏真实世界

        #导入本地游戏数据
        with open("data\\players.json", "r", encoding="utf-8") as f:
            self.players = json.load(f)

        #添加新玩家时的基础数据
        self.settings=Settings()
        self.new_player_data= self.settings.new_player_data
        self.daoju_set=self.settings.daoju_set
        self.job_earn=self.settings.job_earn
    def data_update(self):

        # 写入数据
        with open("data\\players.json", "w", encoding="utf-8") as f:
            json.dump(self.players, f, ensure_ascii=False, indent=4)
        # 读取并更新数据
        with open("data\\players.json", "r", encoding="utf-8") as f:
            self.players = json.load(f)



    def player_work(self,player_qq,group_qq,sessionKey):    #这个是玩家工作时调用的函数
        now_time = time.time()
        try:
            player_qq = str(player_qq)
            player_data = self.players[player_qq]
            first_key = list(self.players[player_qq]['jobset'].keys())[0]
#           这里的判断主要是看玩家的工作cd到没有，如果到了，就可以工作，没到就返回太频繁了
            if now_time - player_data['lasttime'] >=self.players[player_qq]['jobset'][first_key]['work_cd']:
                print(13321)
                with self.file_lock:
                    player_data['cash'] += self.players[player_qq]['jobset'][first_key]['work_salary']
                    player_data['lasttime'] = now_time
                self.data_update()
                group_qq = int(group_qq)
                qq = int(player_qq)
                back_text=' '+self.players[player_qq]['jobset'][first_key]['working_situation']
                self.Group_operate.sendmeassage_group(group_qq, qq, back_text, ' ', ' ',sessionKey)
            else:
                group_qq = int(group_qq)
                qq = int(player_qq)
                self.Group_operate.sendmeassage_group(group_qq, qq, ' 你刚刚才工作完，歇一会儿再来吧', ' ', ' ',sessionKey)
        #永远不要忘了打印报错，这样才能更快的查到错误点
        except Exception as e:
            print('Error:',e)
            group_qq = int(group_qq)
            qq = int(player_qq)
            self.Group_operate.sendmeassage_group(group_qq, qq,' 你还没创建角色呢，快@我创建新角色试试吧', ' ',' ', sessionKey)


#
    def rob_player(self,rober,robbed_player,group_qq,sessionKey):#这个函数用来抢劫别人
        wuli_cha=self.players[str(rober)]['武力值']-self.players[str(robbed_player)]['武力值']
        now_time=time.time()
        if rober!=robbed_player:
            if now_time-self.players[str(robbed_player)]['robbed_lasttime']>=300 and now_time-self.players[str(rober)]['roblasttime']>=600:
                if self.players[str(robbed_player)]['cash']<=0:
                    backtext='\n但是他已经没钱啦'
                elif wuli_cha>=0 and self.players[str(robbed_player)]['cash']>0:
                    money_up=self.players[str(robbed_player)]['cash']-wuli_cha
                    with self.file_lock:
                        try:
                            money_rob=random.randint(0,money_up)
                            money_rob+=wuli_cha
                        except:
                            money_rob=self.players[str(robbed_player)]['cash']
                        self.players[str(robbed_player)]['cash']-=money_rob
                        self.players[str(rober)]['cash']+=money_rob
                        self.players[str(rober)]['roblasttime']=now_time
                        self.players[str(robbed_player)]['robbed_lasttime']=now_time
                        backtext='\n抢走了'+str(money_rob)
                        self.data_update()


                elif wuli_cha < 0 < self.players[str(robbed_player)]['cash']:
                    backtext='\n但是被反揍了一顿'
                    with self.file_lock:
                        self.players[str(rober)]['roblasttime']=now_time
                        self.players[str(rober)]['health']+=wuli_cha
                        self.data_update()



                else:
                    backtext='\n出bug了'
                group_qq = int(group_qq)
                qq = int(rober)
                target=int(robbed_player)
                url = "http://localhost:8080/sendGroupMessage"
                send_message = {
                    "sessionKey": sessionKey,
                    "target": group_qq,
                    "messageChain": [
                        {"type": "At", "target": qq, "display": "@Mirai"},
                        {"type": "Plain", "text": ' 尝试抢劫 '},
                        {"type": "At", "target": target, "display": "@Mirai"},
                        {"type": "Plain", "text": backtext},
                    ]
                }
                res = requests.post(url, json=send_message)
            else:
                group_qq = int(group_qq)
                qq = int(rober)
                target=int(robbed_player)
                url = "http://localhost:8080/sendGroupMessage"
                self.Group_operate.sendmeassage_group(group_qq,qq,' 歇一会儿吧，抢劫太频繁了小心被抓\n（你才抢过别人或者他刚被抢）',' ',' ',sessionKey)
    def view_player_datas(self, player_qq, group_qq, sessionKey):
        try:
            player_qq=str(player_qq)

            self.data_update()

            player_data=self.players[player_qq]
            back_text=('\n你是一名 ' +list(self.players[player_qq]['jobset'].keys())[0] + '\n你身上的现金有 ' +
                str(player_data['cash'])+'\n你的银行存款有 '+str(player_data['bank_money'])+'\n你持有武器 '+
                player_data['weapon']+'\n你的武力值为 '+ str(player_data['武力值'])+'\n'+'你的背包中有：\n')
            back_text=str(back_text)
            print(type(back_text))
            for good_name, good_view in self.players[player_qq]['背包'].items():
                back_text+='\t\t\t'+good_name+':'+' '+str(good_view['数量'])
        except Exception as e:
            print(e)
            back_text='你还没创建角色呢'
        group_qq = int(group_qq)
        qq = int(player_qq)
        self.Group_operate.sendmeassage_group(group_qq, qq, back_text, ' ', ' ', sessionKey)

    def use_daoju(self,player_qq,group_qq,daoju_name,sessionKey):
        try:
            used_success=False
            m=self.players[str(player_qq)]
            player_qq=str(player_qq)
            with self.file_lock:
                try:
                    self.players[player_qq]['背包'][daoju_name]['数量'] -=1
                    back_text='\n道具使用成功（有什么效果呢？，自己探索吧，作者还没做好）'
                    for key,value in self.players[player_qq]['背包'][daoju_name]['效果'].items():
                        self.players[player_qq][key]+=value
                    if self.players[player_qq]['背包'][daoju_name]['数量'] ==0:
                        del self.players[player_qq]['背包'][daoju_name]
                        back_text+='\n该道具已使用完'
                except Exception as e:
                    print(e)
                    back_text = '\n你没有这样道具'
            self.data_update()
        except Exception as e:
            back_text='\n你还没有创建角色呢，快@我创建新角色吧'
            print(e)
        self.Group_operate.sendmeassage_group(group_qq,player_qq,back_text,' ',' ',sessionKey)



    def buy_friut_knief(self,buy_player,group_qq,sessionKey):
        try:
            buy_player_str = str(buy_player)
            cash=self.players[buy_player_str]['cash']
            weapon = self.players[buy_player_str]['weapon']
            if not weapon=='破旧的水果刀':
                if cash>=500:
                    with self.file_lock:
                        self.players[buy_player_str]['cash'] -= 500
                        self.players[buy_player_str]['weapon']='破旧的水果刀'
                        self.players[buy_player_str]['武力值']+=3
                        self.data_update()

                    back_text = ' 购买成功'
                else:
                    back_text=' 你没有那么多现金（只能使用现金购买武器）'
            else:
                back_text=' 你已经有这样武器了'
        except:
            back_text=' 创建新角色了吗你，就来买刀'
        group_qq = int(group_qq)
        qq = int(buy_player)
        self.Group_operate.sendmeassage_group(group_qq, qq, back_text, ' ', ' ', sessionKey)




    def new_player(self,new_player_qq,group_qq,sessionKey):
        new_player_qq=str(new_player_qq)
        if new_player_qq  not in self.players.keys():
            with self.file_lock:
                self.players.update({str(new_player_qq):self.new_player_data})

            self.data_update()
            group_qq = int(group_qq)
            qq = int(new_player_qq)
            self.Group_operate.sendmeassage_group(group_qq, qq,' 创建新角色成功', ' ',' ', sessionKey)

        else:
            group_qq = int(group_qq)
            qq = int(new_player_qq)
            self.Group_operate.sendmeassage_group(group_qq, qq,' 已经创建过角色啦，快去开始游戏吧', ' ',' ', sessionKey)

    def cun_money(self,group_qq,cun_player,cun_player_will,sessionKey):
        try:
            cun_player_str=str(cun_player)
            cash=self.players[cun_player_str]['cash']
            if cash>=int(cun_player_will)+ int(cun_player_will)//10 :
                if int(cun_player_will)%100==0:
                    with self.file_lock:
                        self.players[cun_player_str]['cash']-=int(cun_player_will)+ int(cun_player_will)//10
                        self.players[cun_player_str]['bank_money']+=int(cun_player_will)
                        self.players['1637664832']['bank_money']+=int(cun_player_will)//10
                        self.data_update()
                        back_text='已存入'+str(cun_player_will)
                else:
                    back_text='请存入整百数'

            else:
                back_text='你没有那么多钱（注意手续费）'
            group_qq = int(group_qq)
            qq = int(cun_player)
            self.Group_operate.sendmeassage_group(group_qq, qq,' '+back_text, ' ',' ', sessionKey)

        except Exception as e:
            print(e)


    def qu_money(self,group_qq,qu_player,qu_player_will,sessionKey):
        try:
            qu_player_str=str(qu_player)
            cash=self.players[qu_player_str]['cash']
            bank_money=self.players[qu_player_str]['bank_money']
            if (cash>= int(qu_player_will)//10) and (int(qu_player_will)<=bank_money):
                if int(qu_player_will)%100==0:
                    with self.file_lock:
                        self.players[qu_player_str]['cash']+=(int(qu_player_will)- int(qu_player_will)//10)
                        self.players[qu_player_str]['bank_money']-=int(qu_player_will)
                        self.players['1637664832']['bank_money']+=int(qu_player_will)//10
                        self.data_update()

                    back_text='已取出'+str(qu_player_will)
                else:
                    back_text='请取出整百数'

            else:
                back_text='你没有那么多钱（注意手续费）'
            group_qq = int(group_qq)
            qq = int(qu_player)
            self.Group_operate.sendmeassage_group(group_qq, qq,' '+back_text, ' ',' ', sessionKey)
        except Exception as e:
            print(e)

    def qian_dao(self,group_qq,qq_sender,sessionKey):
        try:
            lasttime=self.players[str(qq_sender)]['last_qiandao_time']
            # 获取当前时间戳
            timestamp = time.time()
            # 格式化本地时间为字符串
            date_str = time.strftime("%Y.%m.%d", time.localtime(timestamp))
            if lasttime==date_str:
                back_text='\n今天已经签过到啦，明天再来吧'
            else:
                self.players[str(qq_sender)]['cash']+=20
                self.players[str(qq_sender)]['last_qiandao_time'] = date_str
                print(13)
                back_text='\n签到成功，不过没有奖励（人家还没做好啦）\n欸欸欸，别打我呀\n这里还有二十块钱和三个个泡芙，都给你吧\n别一次性吃太多哟\n鼠鼠在这里祝你度过愉快的一天'
                with self.file_lock:
                    print(14)
                    self.add_daoju(qq_sender,group_qq,'泡芙',3,sessionKey)
            self.data_update()
            self.Group_operate.sendmeassage_group(group_qq,qq_sender,back_text,' ',' ',sessionKey)
        except Exception as e:
            print(e)

    def shut_up(self,group_qq,qq,qq_sender,sessionKey):
        try:
            player_operate=self.players[str(qq_sender)]
            '''if  player_operate['cash']>=50:
                player_operate['cash']-=50
                target = int(group_qq)
                qq = int(qq)
                url = "http://localhost:8080/mute"
                shut = {
                    "sessionKey": sessionKey,
                    "target": group_qq,
                    "memberId": qq,
                    "time": 60

                }
                res = requests.post(url, json=shut)

                self.data_update()
                back_text=' 禁言目标成功'
                '''

        except Exception as e:
            print(e)
            back_text=' @我创建新角色即可使用该功能'

        target = int(group_qq)
        qq = int(qq)
        url = "http://localhost:8080/sendGroupMessage"
        send_message = {
            "sessionKey": sessionKey,
            "target": int(target),
            "messageChain": [
                {"type": "At", "target": qq_sender ,"display": "@Mirai"},
                {"type": "Plain", "text": back_text},
            ]
        }
        res = requests.post(url, json=send_message)


    #这个函数用来转账
    def zhuanzhang(self,send_player,receiver_player,group_qq,target_money,sessionKey):
        try:
            qq_send_player=self.players[str(send_player)]['bank_money']
            if qq_send_player-int(target_money)>=0 and int(target_money)>=0:
                with self.file_lock:
                    self.players[str(send_player)]['bank_money']-=int(target_money)
                    self.players[str(receiver_player)]['bank_money'] += int(target_money)
                    back_text='转账成功\n你的账户余额还有： '+str(self.players[str(send_player)]['bank_money'])+'\n对方的账户余额'\
                                        '还有： '+str(self.players[str(receiver_player)]['bank_money'])
            else:
                back_text=' 格式错误(请注意余额且不要输入负数）'


            self.data_update()
        except Exception as e:
            print(e)
            back_text=' 出bug了'
        self.Group_operate.sendmeassage_group(group_qq,send_player, back_text, ' ', ' ', sessionKey)

    def add_daoju(self,player_qq,qq_group,daoju,add_num_daoju,sessionKey):
        try:
            player_qq=str(player_qq)
            if daoju not in self.players[player_qq]['背包'].keys():
                new_daoju={daoju:self.daoju_set[daoju]}
                new_daoju[daoju]['数量']=int(add_num_daoju)
                self.players[player_qq]['背包'].update(new_daoju)
            else:
                self.players[player_qq]['背包'][daoju]['数量']+=int(add_num_daoju)
            self.data_update()
            back_text='\n恭喜你获得道具'+daoju+str(add_num_daoju)+' 个'
            self.Group_operate.sendmeassage_group(qq_group,player_qq,back_text,' ',' ',sessionKey)
        except Exception as e:
            print(e)









#以下是猜数字游戏的函数

    def start_game(self,group_qq,qq,sessionKey):
        if self.guess_number==False:
            self.target_number=int(random.randint(1,500))
            group_qq = int(group_qq)
            qq = int(qq)
            self.Group_operate.sendmeassage_group(group_qq, qq,' 请猜一个数字（1，500）', ' ',' ', sessionKey)
            self.guess_number=True
        else:
            qq = int(qq)
            self.Group_operate.sendmeassage_group(group_qq, qq,' 游戏已经开始啦，赶紧猜数字吧！', ' ',' ', sessionKey)
    def cai(self,group_qq,qq,num_cai,sessionKey):
        if self.guess_number==True:
            if num_cai==' 不玩了':
                msg=' 好吧，下次想玩了再@我'
                self.guess_number=False
            else:
                try:
                    num_cai=num_cai.strip()
                    num_cai=num_cai.replace(' ','')
                    num_cai=int(num_cai)
                    if num_cai<self.target_number:
                        msg=' 太小了'
                    elif num_cai>self.target_number:
                        msg=' 太大了'
                    else:
                        msg=' 恭喜你，猜对啦'
                        self.guess_number = False
                except:
                    msg=' 请输入纯数字'
            qq = int(qq)
            self.Group_operate.sendmeassage_group(group_qq, qq,msg, ' ',' ', sessionKey)

    def start_game_friend(self,qq,sessionKey):
        if self.guess_number_friend==False:
            self.target_number_friend=int(random.randint(1,500))
            qq = int(qq)
            url = "http://localhost:8080/sendFriendMessage"
            send_message = {
                "sessionKey": sessionKey,
                "target": qq,
                "messageChain": [
                    {"type": "Plain", "text": ' 请猜一个数字（1，500）'},
                ]
            }
            res = requests.post(url, json=send_message)
            self.guess_number_friend=True
        else:
            qq = int(qq)
            url = "http://localhost:8080/sendFriendMessage"
            send_message = {
                "sessionKey": sessionKey,
                "target": qq,
                "messageChain": [
                    {"type": "At", "target": qq, "display": "@Mirai"},
                    {"type": "Plain", "text": ' 游戏已经开始啦，赶紧猜数字吧！\n如果不是你在玩请耐心等待他人游戏结束'},
                ]
            }
            res = requests.post(url, json=send_message)
            self.guess_number=True
    def cai_friend(self,qq,num_cai,sessionKey):
        if self.guess_number_friend==True:
            if num_cai=='不玩了':
                print(self.target_number_friend)
                msg=' 好吧，下次想玩了再找我'+str(self.target_number_friend)
                self.guess_number_friend=False
            else:
                try:
                    num_cai=num_cai.strip()
                    num_cai=num_cai.replace(' ','')
                    num_cai=int(num_cai)
                    if num_cai<self.target_number_friend:
                        msg=' 太小了'
                    elif num_cai>self.target_number_friend:
                        msg=' 太大了'
                    else:
                        msg=' 恭喜你，猜对啦'
                        self.guess_number_friend = False
                except:
                    msg=' 请输入纯数字\n如果不是你在玩请耐心等待他人游戏结束'
            qq = int(qq)
            url = "http://localhost:8080/sendFriendMessage"
            send_message = {
                "sessionKey": sessionKey,
                "target": qq,
                "messageChain": [
                    {"type": "Plain", "text": msg},
                ]
            }
            res = requests.post(url, json=send_message)