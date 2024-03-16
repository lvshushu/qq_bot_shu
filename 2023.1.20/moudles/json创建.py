import json
import threading
import time
import os

players = json.load(open("data\\players.json", "r", encoding="utf-8"))

try:
    '''
    此处代码用来买到刀

    players['2848516645']['cash']-=500
    players['2848516645']['武力值'] +=3
    players['2848516645']['weapon']='破旧的水果刀'

                '''

    '''
    此处代码用来存钱
   
    players['2087374501']['cash'] -=4700
    players['2087374501']['bank_money']+=4700
    players['1637664832']['bank_money']+=160

             '''


    '''
    #此处代码用来改群主的数值

    players['2320864323']['weapon'] ='未来战士装甲'
    players['2320864323']['武力值']=100


    '''
    #players['1637664832']['jobset'] = {'货运司机':
             #              {'working_situation':'辛苦地拉完一车货后，你获得了68块',
              #              'work_cd':500,
                     #       'work_salary':68
                 #           }
                       #            }
    #del players['3067559135']
    #del players['2062926551']
    #del players['1637664832']






    '''

    
  
     #此处代码用来为所有玩家初始化某样值
     #初始化职业
        
        players['']['jobset'] = {'环卫工人':
                           {'working_situation':'辛苦地扫完大街后，你获得了30块',
                            'work_cd':300,
                            'work_salary':30
                            }
                                   }
     
     for key,valu in players.items():
            valu['roblasttime']=0
            valu['robbed_lasttime']=0
            valu['health']=100
           # valu.update({'roblasttime':100})
    '''


    with open("data\\players.json", "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=4)



except Exception as e:
    print(e)
    print('出bug了')






