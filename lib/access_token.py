# -*- coding: utf-8 -*-
import jwt
import time
from lib.ini_info import *

issuer, key, expiration_time = get_info()


def create_token(openid):
    d = {
        # 公共声明
        'exp': time.time() + expiration_time,  # (Expiration Time) 此token的过期时间的时间戳
        'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
        'iss': issuer,  # (Issuer) 指明此token的签发者
        # 私有声明
        'data': {
            'openid': openid,
            'timestamp': time.time(),
        }
    }


    token = jwt.encode(d, key, algorithm='HS256')

    return token


def decode_token(token):
    res = jwt.decode(token, key, issuer=issuer, algorithms=['HS256'])
    return res
