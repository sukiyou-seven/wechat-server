import os

from lib.ini_info import DB_INFO

db_info = DB_INFO()

table_list = [
    "gloable_data"
]
for x in table_list:
    print(x + '\r')
    command = "sqlacodegen  --outfile " + x + ".py --table " + x + f" mysql+pymysql://{db_info.get('user')}:{db_info.get('pwd')}@{db_info.get('host')}:{db_info.get('port')}/{db_info.get('dbname')}?charset=utf8mb4"
    os.system(command)
    print(command)