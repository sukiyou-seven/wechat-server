
from flask import Flask
from lib.blueprint_info import *

app = Flask(__name__, static_folder="./../static")
# 蓝图注册
    