# -*- coding: utf-8 -*-
import configparser
import os


class readini:
	def __init__(self, file="db.ini"):
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件目录
		self.ConfigPath = os.path.join(self.BASE_DIR, '../config')  # 自己的配置文件路径，根据项目需求，这里是--> 在当前目录下的config下存放目录文件
		self.slat = "IchLiebeWangLanPink"
		self.conf = configparser.ConfigParser()
		self.file_name = file
		self.file_path = os.path.join(self.ConfigPath, self.file_name)
		...

	def readr(self, pal='mysql'):
		"""
		:param pal: sectionName
		:return:
		"""
		self.conf.read(self.file_path, encoding="utf-8")  # python3
		res = self.conf.items(pal)
		t = {}
		for x in res:
			x = list(x)
			p = {x[0]: x[1]}
			t.update(p)
		return t
		