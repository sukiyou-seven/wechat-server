# coding: utf-8
from models.ex_import import *

# design by seven  2023-02-23 15:40:27


class NameList(Base,CUdr):
    __tablename__ = 'name_list'

    id = Column(INTEGER(11), primary_key=True)
    item = Column(String(50))
    avatarurl = Column(String(500))
