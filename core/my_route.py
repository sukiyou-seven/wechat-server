from lib.main_app import app, sukiyou_global

from interface.user import *
from interface.user_bill import *


@app.route('/login', methods=['POST'])
def login():
    res = user().logins(request.get_json())
    print(f"res=>{res}")
    return res


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    res = user().register(data)
    return res


@app.route('/save-idcard', methods=['POST'])
def avedcard():
    res = user().save_idcard(request.get_json())
    return res


@app.route('/get-bill', methods=['POST'])
def get_bill():
    res = user_bill().get_bill(request.get_json())
    return res


@app.route('/create-bill', methods=['POST'])
def create_bill():
    res = user_bill().create_bill_by_user(request.get_json())
    if res != 0:
        return [f"请在 {res} 秒后再试"]
    else:
        return ['The bill is generated successfully. Please return and go to the bill page']
