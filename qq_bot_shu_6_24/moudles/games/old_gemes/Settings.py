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



        #后面的部分用来存储Games的基础设置
        self.new_player_data={'lasttime':0.0,
                       'weapon':'无',
                       'cash':100,
                       'bank_money':0,
                       'job':'环卫工人',
                       'jobset' :{'环卫工人':
                           {'working_situation':'辛苦地扫完大街后，你获得了30块',
                            'work_cd':300,
                            'work_salary':30
                            }
                                   },
                       '武力值':5,
                       'health':100,
                       'roblasttime':0,
                       'robbed_lasttime':0,
                       'last_qiandao_time': "2023.1.1",
                              '背包':{'炒饭':{
                                            '数量':3,
                                            '物品描述':'香喷喷的炒饭',
                                            '效果':{'health':10,'roblasttime':-200,'lasttime':-300}
                                              }

                              }

                              }
        #这里用来存储道具属性
        self.daoju_set = {'炒饭': {
            '数量': 1,
            '物品描述': '香喷喷的炒饭',
            '效果': {'health': 10, 'roblasttime': -200, 'lasttime': -300}
        },
            '彩票': {
                '数量': 1,
                '物品描述': '不劳而获的诱惑，你能抵挡得住吗',
                '效果': {'roblasttime': -300, 'lasttime': +240, 'cash': random.randint(1, 80)}
            },
            '四级必过小药丸': {
                '数量': 1,
                '物品描述': '四级必过',
                '效果': {'roblasttime': +600, 'lasttime': -600, 'cash': random.randint(100, 200)}
            },

            '小蛋糕': {
                '数量': 1,
                '物品描述': '香喷喷的小蛋糕',
                '效果': {'roblasttime': -600, 'lasttime': -300, 'health': -1}
            },

            '泡芙': {
                '数量': 1,
                '物品描述': '香喷喷的泡芙，一口下去全是奶油',
                '效果': {'roblasttime': -1000, 'lasttime': 300, 'health': -2}
            }
        }


        self.job_earn={'环卫工人':
                           {1:['辛苦地扫完大街后，你获得了50块',30,300]
                            },
                       '货运司机':{1:['辛苦地拉完一车货后，你获得了68块',68,240]
                            }
                            }

        self.last_news={}#key是群号，value是上一条消息




        self.news_chehui={}#key是id,value是时间