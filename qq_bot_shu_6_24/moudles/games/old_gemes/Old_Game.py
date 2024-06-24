from moudles.common_funcation import *
from moudles.group.common_function_group import *
from moudles.games.old_gemes.Settings import Settings
import random
import requests
import threading
import time
import json
class Games:#游戏真实事件
    def __init__(self):
        #游戏猜数字
        self.guess_number=False
        self.target_number=0
        self.guess_number_friend=False
        self.target_number_friend=0
        self.file_lock = threading.Lock()


        #导入本地游戏数据
        with open("data/games/真实世界.json", "r", encoding="utf-8") as f:
            self.players = json.load(f)

        #添加新玩家时的基础数据
        self.settings=Settings()
        self.new_player_data= self.settings.new_player_data
        self.daoju_set=self.settings.daoju_set
        self.job_earn=self.settings.job_earn
    def data_update(self):

        # 写入数据
        with open("data/games/真实世界.json", "w", encoding="utf-8") as f:
            json.dump(self.players, f, ensure_ascii=False, indent=4)
        # 读取并更新数据
        with open("data/games/真实世界.json", "r", encoding="utf-8") as f:
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
                sendmeassage_group(group_qq, message_chain_make_at(back_text,qq),sessionKey)
            else:
                group_qq = int(group_qq)
                qq = int(player_qq)
                sendmeassage_group(group_qq,message_chain_make_at(' 你刚刚才工作完，歇一会儿再来吧',qq),sessionKey)
        #永远不要忘了打印报错，这样才能更快的查到错误点
        except Exception as e:
            print('Error:',e)
            group_qq = int(group_qq)
            qq = int(player_qq)

            sendmeassage_group(group_qq, message_chain_make_at(' 你还没创建角色呢，快@我创建新角色试试吧',qq), sessionKey)


#
    def rob_player(self,rober,robbed_player,group_qq,sessionKey):#这个函数用来抢劫别人
        wuli_cha=self.players[str(rober)]['武力值']-self.players[str(robbed_player)]['武力值']
        wuli_cha+=random.randint(-5,6)
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
                sendmeassage_group(group_qq, message_chain_make_at(' 歇一会儿吧，抢劫太频繁了小心被抓\n（你才抢过别人或者他刚被抢）', qq),
                                   sessionKey)
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
        sendmeassage_group(group_qq,
                           message_chain_make_at(back_text, qq),
                           sessionKey)

    def use_daoju(self,player_qq,group_qq,daoju_name,sessionKey):
        try:
            used_success=False
            m=self.players[str(player_qq)]
            player_qq=str(player_qq)
            with self.file_lock:
                try:
                    self.players[player_qq]['背包'][daoju_name]['数量'] -=1
                    back_text='\n道具使用成功（有什么效果呢？，自己探索吧，作者还没做好）'
                    if daoju_name=="彩票":
                        self.daoju_set[daoju_name]['效果']["cash"]=random.randint(1,120)
                        back_text+=(" \n等等，原来这是张彩票啊，我帮你刮开吧，芜湖，恭喜你中了%s元，请我一块钱买辣"
                                    "条吧欧皇")%(str(self.daoju_set[daoju_name]['效果']["cash"]+1))
                    for key,value in self.daoju_set[daoju_name]['效果'].items():
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
        sendmeassage_group(group_qq,
                           message_chain_make_at(back_text, player_qq),
                           sessionKey)



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
        sendmeassage_group(group_qq,
                           message_chain_make_at(back_text, qq),
                           sessionKey)




    def new_player(self,new_player_qq,group_qq,sessionKey):
        new_player_qq=str(new_player_qq)
        if new_player_qq  not in self.players.keys():
            with self.file_lock:
                self.players.update({str(new_player_qq):self.new_player_data})

            self.data_update()
            group_qq = int(group_qq)
            qq = int(new_player_qq)
            sendmeassage_group(group_qq,
                               message_chain_make_at(" 创建新角色成功", qq),
                               sessionKey)

        else:
            group_qq = int(group_qq)
            qq = int(new_player_qq)
            sendmeassage_group(group_qq,
                               message_chain_make_at(" 已经创建过角色啦，快去开始游戏吧", qq),
                               sessionKey)

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
                    back_text=' 请存入整百数'

            else:
                back_text=' 你没有那么多钱（注意手续费）'
            group_qq = int(group_qq)
            qq = int(cun_player)
            sendmeassage_group(group_qq,
                               message_chain_make_at(back_text, qq),
                               sessionKey)

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
                back_text=' 你没有那么多钱（注意手续费）'
            group_qq = int(group_qq)
            qq = int(qu_player)
            sendmeassage_group(group_qq,
                               message_chain_make_at(back_text, qq),
                               sessionKey)
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
                back_text=('\n签到成功，不过没有奖励（人家还没做好啦）\n欸欸欸，别打我呀\n这里还有二十块钱和一张彩票，都给你吧'
                           '\n小赌怡情，大赌伤身\n鼠鼠在这里祝你度过愉快的一天')
                with self.file_lock:
                    self.add_daoju(qq_sender,group_qq,'彩票',1,sessionKey)
            self.data_update()
            sendmeassage_group(group_qq,
                               message_chain_make_at(back_text, qq_sender),
                               sessionKey)
        except Exception as e:
            print(e)

    def shut_up(self,group_qq,qq,qq_sender,sessionKey):
        try:
            player_operate=self.players[str(qq_sender)]
            if  player_operate['cash']>=50:
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

            else:
                back_text=' 你没有那么多钱购买禁言他人功能（一次50）'
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
        sendmeassage_group(group_qq,
                           message_chain_make_at(back_text, send_player),
                           sessionKey)

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
            sendmeassage_group(qq_group,
                               message_chain_make_at(back_text, player_qq),
                               sessionKey)
        except Exception as e:
            print(e)

    def get_text_from_url(self,qq_sender,url,price):
        try:
            player_operate = self.players[str(qq_sender)]
            if player_operate['cash'] >= price:
                player_operate['cash'] -= price
                self.data_update()
                response = requests.get(url)
                return response
            else:
                return True
        except Exception as e:
            print(e)
    def Kfc(self,qq_sender,qq_group,sessionKey):
        try:
            data_json=self.get_text_from_url(qq_sender,"https://api.shadiao.pro/kfc",50)
            self.data_update()
            back_text = (data_json.json()["data"]["text"])
        except Exception as e:
            back_text = ' 你没有那么多钱购买疯狂星期四文案（一次50）'
        sendmeassage_group(qq_group,
                           message_chain_make(back_text),
                           sessionKey)

    def green_tea(self,qq_sender,qq_group,sessionKey):
        try:
            data_json=self.get_text_from_url(qq_sender,"https://api.lovelive.tools/api/SweetNothings/Web/0",5)
            self.data_update()
            back_text = (data_json.json()["returnObj"]["content"])
        except Exception as e:
            back_text = ' 你没有那么多钱购买绿茶文案（一次5）'
        sendmeassage_group(qq_group,
                           message_chain_make_at(back_text,qq_sender),
                           sessionKey)

    def sea_love(self,qq_sender,qq_group,sessionKey):
        try:
            data_json=self.get_text_from_url(qq_sender,"https://api.lovelive.tools/api/SweetNothings/Web/1",5)
            self.data_update()
            back_text = (data_json.json()["returnObj"]["content"])
        except Exception as e:
            back_text = ' 你没有那么多钱购买海王文案（一次5）'
        sendmeassage_group(qq_group,
                           message_chain_make_at(back_text,qq_sender),
                           sessionKey)

    def main(self, q_list, qq_sender, qq_group, sessionKey,at,bot_qq):
        if '抢劫' in q_list[0]:
            self.rob_player(qq_sender, at, qq_group, sessionKey)
        elif at == bot_qq and q_list[0] == ' 创建新角色':
            print(1)
            self.new_player(qq_sender, qq_group, sessionKey)
        elif at == bot_qq and q_list[0] == ' 我要工作':
            self.player_work(qq_sender, qq_group, sessionKey)
        elif at == bot_qq and q_list[0] == ' 查看信息':
            self.view_player_datas(qq_sender, qq_group, sessionKey)
        elif at == bot_qq and q_list[0] == ' 签到':
            self.qian_dao(qq_group, qq_sender, sessionKey)
        elif at == bot_qq and ' 我要存款' in q_list[0]:
            result = q_list[1]
            self.cun_money(qq_group, qq_sender, result, sessionKey)
        elif at == bot_qq and ' 使用道具' in q_list[0]:
            result = q_list[1]
            self.use_daoju(qq_sender, qq_group, result, sessionKey)
        elif at == bot_qq and ' 我要取钱' in q_list[0]:
            result = q_list[1]
            self.qu_money(qq_group, qq_sender, result, sessionKey)
        elif ' 转账' in q_list[0]:
            result = q_list[1]
            self.zhuanzhang(qq_sender, at, qq_group, result, sessionKey)
        elif ' 更新数据' in q_list[0]:
            with open("data/games/真实世界.json", "r", encoding="utf-8") as f:
                self.players = json.load(f)
        elif at == bot_qq and q_list[0] == ' 购买破旧的水果刀':
            self.buy_friut_knief(qq_sender, qq_group, sessionKey)
        elif at == bot_qq and q_list[0] == ' 疯狂星期四':
            self.Kfc(qq_sender,qq_group,sessionKey)
        elif at == bot_qq and q_list[0] == ' 茶我':
            self.green_tea(qq_sender,qq_group,sessionKey)
        elif at == bot_qq and q_list[0] == ' 海我':
            self.sea_love(qq_sender,qq_group,sessionKey)