#来吧，重构这个游戏
import random as r
import moudles.common_funcation
from moudles.common_funcation import *
class Eat_beans:
	def __init__(self):
		self.enemy=None
		self.player=None
		self.技能名库=["豆","毒","枪","防"]
		self.技能库={
			"豆":{
				"spend":-1,
				"attack":0,#貌似没有必要，再看看\
				"varies":0

			}
		}

