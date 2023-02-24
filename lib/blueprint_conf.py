# -*- coding: utf-8 -*-
from lib.ini_info import blue_print_info

import os

res = blue_print_info()
with open('lib/blueprint_register.py', 'w', encoding='utf-8') as f:
    f.write(f"""
from flask import Flask
from lib.blueprint_info import *

app = Flask(__name__, static_folder="./../static")
# 蓝图注册
    """)
    f.close()

with open('lib/blueprint_info.py', 'w', encoding='utf-8') as f:
    f.write(f"""
from flask import Blueprint
        """)
    f.close()
for x in res:
    with open('lib/blueprint_info.py', 'a', encoding='utf-8') as f:
        f.write(f"""
{x} = Blueprint('{x}', __name__, url_prefix="/{res[x]}")
        """)
        f.close()

    with open('lib/blueprint_register.py', 'a', encoding='utf-8') as f:
        f.write(f"""
app.register_blueprint({x})
    """)
        f.close()
        pass

    pass
