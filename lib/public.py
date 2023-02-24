import hashlib
import os
import time
import json

import requests


def del_uploads__(url):
    url_list = url.split('/')
    print(url_list)
    try:
        # 找到文件名
        for x in url_list:
            if x.find('?') != -1:
                # 删除他
                t = x.split('?')
                for p in t:
                    if p.find('.') != -1:
                        os.remove(os.getcwd() + "/static/" + p)
        return "文件删除成功"
    except Exception as e:
        return f"文件删除失败 ==> {e}"

    pass


def get_loca_time():
    """
    :return: "%Y-%m-%d %H:%M:%S"
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def su_sha256(data):
    hashs = hashlib.sha256()
    hashs.update(data.encode('utf-8'))
    return hashs.hexdigest()


def decode_aes(e):
    url = "https://h5.rubyonly.cn/php_aes/index.php"
    # url = "http://localhost/aes/aes.php"
    data = {
        'data': e['encryptedData'],
        'key': e['key'],
        'iv': e['iv'],
        'type': 'de',
    }
    res = requests.post(url, data)
    return json.loads(res.text)
