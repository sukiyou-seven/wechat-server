from interface.interface_import import *

from models.user import *

from lib.public import su_sha256


class user:
    def __init__(self):
        self.session = DbSession()

        pass

    def logins(self, data):
        username = data.get('username')
        password = data.get('password')
        password = su_sha256(password)
        filt = {
            User.username == username,
            User.password == password
        }

        res = User.fetch_one(session=self.session, filter=filt)
        if not res:
            return [False]

        return res

    def register(self, data):
        username_ = data.get('username')
        password_ = data.get('password')

        password_ = su_sha256(password_)

        emps = User(
            username=username_,
            password=password_
        )

        res = User.insert(emps)
        if res:
            return [res]
        else:
            return ['用户名已存在']

    def save_idcard(self, data):
        img_list = data.get('img_list')['value']
        username = data.get('username')
        if len(img_list) < 2:
            return ["证件照片缺失"]

        i_z = img_list[0]
        i_f = img_list[1]

        filt = {
            User.username == username,
            User.is_use == 0
        }

        update_ = {
            'idcard_f': i_z,
            'idcard_z': i_f,
            'is_use': 1
        }

        res, num = User.update(filter=filt, update=update_)
        if res:
            if num > 0:
                return ['数据更新成功']
            else:
                return ['未更新数据，数据不允许被更改']
        else:
            return [res]

    def user_pass(self, data):
        id = data.get('id')
        filt = {
            User.id == id
        }
        update_ = {
            'is_pass': 1
        }
        res, num = User.update(filter=filt, update=update_)
        if res:
            if num > 0:
                return ['数据更新成功']
            else:
                return ['未更新数据,请重新获取数据,数据在之前已被更改']
        else:
            return [res]

