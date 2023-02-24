import os
import time


class errorlogs:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前文件目录
		self.ConfigPath = os.path.join(self.BASE_DIR, '../log')  # 自己的配置文件路径，根据项目需求，这里是--> 在当前目录下的config下存放目录文件
		self.file_name = "app_err_log.log"
		self.file_path = os.path.join(self.ConfigPath, self.file_name)

	def writeLog(self, path, method, text, status):
		writetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		file = open(self.file_path, 'a+', encoding='utf8')
		str='[ time=> (' + writetime + ') ] - [ method=>' + method + ' ] - [ path=>' + path + ' ] - [ error_code=> ' + status + ' ] - [ error_message=> { ' + text + ' } ]  \n'
		file.write(str)
		file.close()

		
		