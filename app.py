from lib.main_app import app, g, __log__
# main_app 内包含一个 '/' 路由用于测试服务是否启动成功
#				一个 after_request方法, 重新格式化返回值及写流水日志
#
# -----------------------------------------------
# -----------------------------------------------
app.run(port=12369, host='0.0.0.0')
'''
keytool -genkey -alias wechat -keyalg RSA -keysize 2048 -validity 36500 -keystore wechat.keystore
'''