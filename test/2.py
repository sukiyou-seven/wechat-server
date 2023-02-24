使用python
不使用 pandas 模块
将下列数据
根据
nickname_time
按年月分组
数据中 当in_out=0时代表支出 in_out=1时代表收入
数据中price为str类型 需要转换类型 否则计算结果为字符串相加
并重新生成一个新的数组
生成的新数组的每一项应包含这一项计算时所用到的源数据项数组
[{'id': 3360, 'avatarurl': '默认头像', 'nickname': '滴滴', 'nickname_time': '2023-02-24 04:46:17', 'price': '5180.30',
  'in_out': 0, 'belong': '12345'}, {'id': 3361, 'avatarurl': '/static/tx/IMG_0004.JPG', 'nickname': '微信红包-来自忧梦',
                                    'nickname_time': '2023-02-24 04:46:17', 'price': '15.50', 'in_out': 1,
                                    'belong': '12345'},
 {'id': 3384, 'avatarurl': '默认头像', 'nickname': '洗澡', 'nickname_time': '2023-01-27 17:57:30', 'price': '1186.51',
  'in_out': 0, 'belong': '12345'},
 {'id': 3385, 'avatarurl': '/static/tx/IMG_0004.JPG', 'nickname': '微信红包-来自为何要爱丶',
  'nickname_time': '2023-01-27 17:57:30', 'price': '9680.86', 'in_out': 1, 'belong': '12345'}]