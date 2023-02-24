# coding: utf-8
from models.ex_import import *

# design by seven  2023-02-24 10:28:58


class GloableDatum(Base,CUdr):
    __tablename__ = 'gloable_data'

    id = Column(INTEGER(11), primary_key=True)
    item = Column(String(200))
    location = Column(INTEGER(11), server_default=text("'1'"))
