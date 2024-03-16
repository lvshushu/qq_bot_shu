import random
import json
class Settings:
    def __init__(self):
        self.ato_reponse_group= json.load(open("data\\ato_reponse_group.json", "r", encoding="utf-8"))
        #群聊关键词自动回复

        self.ato_response_Friend = json.load(open("data\\ato_response_Friend.json", "r", encoding="utf-8"))
        #私信关键词自动回复

        self.ato_geoup_welcome_new_member=json.load(open("data\\ato_group_welcome_new_member.json", "r", encoding="utf-"
                                                                                    "8"))#新人入群自动欢迎

        self.group_lock_id=json.load(open("data\\group_lock_id.json", "r", encoding="utf-8"))#锁定群昵称
        #key为group_id,value为nick_id

        self.message_recall = json.load(open("data\\message_recall.json", "r", encoding="utf-8"))

        self.group_settings=json.load(open("data\\group_settings.json","r",encoding="utf-8"))

        self.group_open_or_not=json.load(open("data\\group_or_not.json","r",encoding="utf-8"))#存储群聊相关的功能开关代码

        #后面的部分用来存储Games的基础设置
        self.new_player_data=json.load(open("data\\game_world\\new_player_data.json","r",encoding="utf-8"))
        #这里用来存储道具属性
        self.daoju_set = json.load(open("data\\game_world\\daoju_set.json","r",encoding="utf-8"))


        self.job_earn={'环卫工人':
                           {1:['辛苦地扫完大街后，你获得了50块',30,300]
                            },
                       '货运司机':{1:['辛苦地拉完一车货后，你获得了68块',68,240]
                            }
                            }

        self.last_news={}#key是群号，value是上一条消息

        self.news_chehui={}#key是id,value是时间