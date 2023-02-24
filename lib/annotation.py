# -*- coding: utf-8 -*-
from functools import wraps
from flask import request
from flask import g as sukiyou_global
from lib.access_token import decode_token


def check_token(f):
	@wraps(f)
	def check():
		data = request.get_json()
		token = data.get('token')
		if token is not None:
			try:
				res = decode_token(token)
				sukiyou_global.openid = res.get("openid")
				sukiyou_global.sukiyou_appid = res.get('sukiyou_appid')
				return f()
			except:
				return ['token has expiration']

			pass
		else:
			return ['token has gone']
	return check

  