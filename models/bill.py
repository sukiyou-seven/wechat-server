# coding: utf-8
from models.ex_import import *

# design by seven  2023-02-23 13:37:09


class Bill(Base,CUdr):
    __tablename__ = 'bill'

    id = Column(INTEGER(11), primary_key=True)
    avatarurl = Column(String(500))
    nickname = Column(String(500))
    nickname_time = Column(TIMESTAMP)
    price = Column(INTEGER(11))
    in_out = Column(INTEGER(11))
    belong = Column(String(36))
