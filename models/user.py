# coding: utf-8
from models.ex_import import *

# design by seven  2023-02-20 13:24:24


class User(Base,CUdr):
    __tablename__ = 'user'
    __table_args__ = {'comment': '用户信息'}

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    userinfo = Column(String(255))
    idcard_z = Column(String(255))
    idcard_f = Column(String(255))
    is_use = Column(Boolean)
    is_pass = Column(Boolean)