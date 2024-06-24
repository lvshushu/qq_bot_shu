import random
from moudles.common_funcation import *
class 人物:
	def __init__(self):
		self.blood=1
		self.dou=0
		self.选择=False

	def main(self):
		pass
	def exchange_qq(self,qq):
		self.qq=str(qq)
	def 出招(self,招式,file):
		if 招式=="豆":
			self.data = read_data(file)
			self.data[self.qq]["blood"]=self.blood
			self.data[self.qq]["dou"]=self.dou
			self.data[self.qq]["出招"]=self.出招
			save_data(self.data,file)
	def update_(self,file):
		self.data=read_data(file)
		self.blood=self.data[self.qq]["blood"]
		self.dou=self.data[self.qq]["dou"]
		self.出招=self.data[self.qq]["出招"]
class 敌人(人物):
	def __init__(self):
		self.name=""

	def suiji_zhaoshi(self):
		pass