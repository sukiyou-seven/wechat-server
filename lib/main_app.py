import json

from flask_cors import *
from flask import g
from lib.errorlog import errorlogs
from lib.access_token import create_token

from lib.annotation import *

#  init server system


# 蓝图
try:
    # 未创建蓝图时 报错时正常的
    from lib.blueprint_conf import *
    from lib.blueprint_info import *
    from lib.blueprint_register import *
except:
    print("当前工作区无蓝图")
    pass

# 文件上传及删除
from lib.blueprint_upload import *

# 注册文件系统
app.register_blueprint(upload)

CORS(app, supports_credentials=True)  # 设置跨域

from core.blueprint_imp import *

# init log system
__log__ = errorlogs()


@app.route('/get-token', methods=['POST'])
def get_token():
    '''
    :param : openid 用户身份标识
    :param : my_appid 本程序的唯一id 随意生成
    :return:
    '''
    data = request.get_json()
    openid = data.get('openid')
    sukiyou_appid = data.get('my_appid')
    return [create_token({
        "openid": openid,
        "sukiyou_appid": sukiyou_appid
    })]


@app.route('/', methods=['POST', 'GET'])
def testfalknsdfjnsf():
    sukiyou_global.message = "success"
    return ["恭喜,安装成功"]


@app.before_request
def __before_requests___():
    pass


@app.after_request
# @check_error_msg
def __after__(response):
    # ------------------- 定义返回值 -----------------------------------------
    try:
        if type(eval(response.data)) is list or type(eval(response.data)) is dict:
            msg = "success"
            if g.get('message'):
                msg = g.get('message')
            response.data = json.dumps({"message": msg, "code": '0', 'data': json.loads(response.data.decode('utf-8'))}, ensure_ascii=False)
            error_code = 0
        else:
            msg = response.data.decode('utf-8')
            response.data = json.dumps(
                {"message": "<route>[ " + request.path + " ]<error>[ " + response.data.decode('utf-8') + " ]",
                 "code": '201',
                 'data': False}, ensure_ascii=False)
            error_code = 201
    except:
        try:

            msg = response.data.decode('utf-8')
            print(msg)
            response.data = json.dumps(
                {"message": "<route>[ " + request.path + " ]<error>[ " + response.data.decode('utf-8') + " ]",
                 "code": '500',
                 'data': False}, ensure_ascii=False)
            error_code = 500
        except:
            msg = "未知 image?"
            error_code = 7
            pass
    # -------------------- 写日志 ---------------------------------------------
    __log__.writeLog(request.path, request.method, str(msg), str(error_code))
    return response
