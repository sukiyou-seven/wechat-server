from collections import defaultdict

from interface.gloable_data import *
from interface.interface_import import *
from interface.radis_ import RedisHelper

from models.user import *
from models.bill import *
from models.name_list import *

# from lib.public import su_sha256

import random
from datetime import datetime, timedelta


class user_bill:
    def __init__(self):
        self.session = DbSession()
        self.avatar_list = []

    def create_bill_by_user(self, data):
        user_uid = data.get('username')
        total_in = data.get('total_in')
        total_out = data.get('total_out')

        res = RedisHelper().ttl__(user_uid)

        if res != -2:
            return res

        RedisHelper().set_key_with_timeout(user_uid, "sukiyou", 300)

        price_in = 0
        price_out = 0

        total_in *= 100
        total_out *= 100

        # 清除历史账单
        a = Bill.delete_real(filter={
            Bill.belong == user_uid
        })

        while True:
            in_, out_ = self.__create_bill__(user_uid)
            price_in += in_
            price_out += out_

            if price_out > total_out and price_in > total_in:
                break

        return 0

    def get_bill(self, data):
        username = data.get('username')
        datetime_ = data.get('datetime')
        page = data.get('page')
        lim = data.get('limit')

        limit = (page, lim)
        if not page:
            limit = False
        if not limit:
            limit = False

        filt = {
            Bill.belong == username
        }
        if datetime_:
            # print("datetime_")
            filt = {
                Bill.belong == username,
                Bill.nickname_time > datetime_
            }

        res = Bill.fetch_all(session=self.session, filter=filt, order=(Bill.nickname_time, True), limit=limit)
        # print(res)

        # for x in res['list']:
        #     x['nickname_time_tmp'] = x['nickname_time']
        #     date_obj = datetime.strptime(x['nickname_time_tmp'] , '%Y-%m-%d %H:%M:%S')
        #     year = date_obj.year
        #     month = date_obj.month

        new_data = defaultdict(list)

        for item in res['list']:
            year_month = item['nickname_time'][:7]  # 提取年月
            price = float(item['price'])  # 转换为浮点型
            new_data[year_month].append({'item': item, 'price': price})  # 按年月分组，并添加到新的数据字典中

        result = []
        for year_month, items in new_data.items():
            total_in = 0
            total_out = 0
            for item in items:
                price = item['price']
                if item['item']['in_out'] == 0:
                    total_out += price
                else:
                    total_in += price
            result.append(
                {'year': year_month[:4], 'month': year_month[5:], 'total_in': round(total_in,2), 'total_out': round(total_out,2),
                 'items': items})


        return result

    def __create_bill__(self, user_uid):
        today = datetime.now()
        offset = timedelta(days=-365)
        re_date = (today + offset).strftime('%Y-%m-%d')
        re_today = today.strftime('%Y-%m-%d')
        # 随机一个日期
        date_ = self.__random_date__(re_date, re_today)
        # 随机一个支出
        price_out = random.randint(1000, 999999)

        # 获取头像列表
        self.avatar_list = gloabel_datas().get_avatar()['list']

        # 随机一个支出的名称
        name_list = self.__get_name_list__()
        name_list = name_list['list']
        random_element = random.choice(name_list)

        avaraturl = random.choice(self.avatar_list)['item']
        # in_out  0 支出  1  收入
        # 构建支出数据
        emps = Bill(
            nickname_time=date_,
            price=price_out,
            in_out=0,
            belong=user_uid,
            nickname=random_element.get('item'),
            avatarurl=avaraturl
        )
        res = Bill.insert(emps)
        # 随机一个收入
        price_in = random.randint(1000, 999999)

        # 随机一个收入的名称
        in_list = gloabel_datas().get_data()['list']
        random_element = random.choice(in_list)

        avaraturl = random.choice(self.avatar_list)['item']

        # 构建收入数据
        emps = Bill(
            nickname_time=date_,
            price=price_in,
            in_out=1,
            belong=user_uid,
            nickname=random_element.get('item'),
            avatarurl=avaraturl
        )
        res2 = Bill.insert(emps)
        return price_in, price_out

    def __random_date__(self, start, end):
        start_list = start.split("-")
        end_list = end.split("-")
        start = datetime(int(start_list[0]), int(start_list[1]), int(start_list[2]))
        end = datetime(int(end_list[0]), int(end_list[1]), int(end_list[2]))

        delta = end - start
        random_date = start + timedelta(days=random.randint(0, delta.days))

        # 随机生成一个时间
        random_time = datetime.strptime(f'{random.randint(0, 23)}:{random.randint(0, 59)}:{random.randint(0, 59)}',
                                        '%H:%M:%S').time()

        # 将随机时间和随机日期合并为一个 datetime 对象
        random_datetime = datetime.combine(random_date.date(), random_time)
        #
        # dt = datetime.strptime(str(random_datetime), "%Y-%m-%d %H:%M:%S")
        #
        # # 将 datetime 对象转换为 UTC 时间戳
        # timestamp = (dt - datetime(1970, 1, 1)) / timedelta(seconds=1)

        return random_datetime

    def __get_name_list__(self):
        res = NameList.fetch_all(session=self.session)
        return res




# if __name__ == '__main__':
# user_bill().create_bill_by_user({
#     "username": "12345",
#     "total_in": 12345,
#     "total_out": 2345
# })

# user_bill().get_bill({
#     "username": "12345",
#     "datetime" : "2023-01-01"
# })
