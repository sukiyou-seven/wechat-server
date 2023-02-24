import json

import requests

from lib.config_r import readini
from lib.public import decode_aes


class wx_inc:
	def __init__(self):
		try:
			self.wxinfo = readini('wx_info.ini').readr('wxinfo')
		except:
			self.wxinfo = False
		if not self.wxinfo:
			return

	def auth_code2session(self, code, data={}):
		url = f"https://api.weixin.qq.com/sns/jscode2session?" \
			  f"appid={self.wxinfo.get('appid')}&" \
			  f"secret={self.wxinfo.get('secret')}&" \
			  f"js_code={code}&" \
			  f"grant_type=authorization_code"
		response = requests.get(url=url)
		response = json.loads(response.text)
		try:
			if response['errcode'] == 0:
				try:
					session_key = response['session_key']
					encryptedData = data['encryptedData']
					iv = data['iv']
					encryptedData_info = decode_aes({'encryptedData': encryptedData, 'key': session_key, 'iv': iv})
					phone = encryptedData_info['phoneNumber']
				except:
					phone = '获取失败'
					pass
				response['phone'] = phone
				return response
			else:
				print(response)
				return response
		except:
			return response

		
		