import datetime
import json
import time

from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from lib.config_r import readini
from lib.ini_info import DB_INFO, upload_host

db_info = DB_INFO()

engine = create_engine(f"mysql+pymysql://{db_info.get('user')}:{db_info.get('pwd')}"
                       f"@{db_info.get('host')}:{db_info.get('port')}/{db_info.get('dbname')}?",
                       echo=False,
                       pool_recycle=-1,  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                       pool_size=10,  # 连接池大小
                       max_overflow=5,  # 超过连接池大小外最多创建的连接
                       pool_timeout=10,  # 池中没有线程最多等待的时间，否则报错
                       isolation_level="READ UNCOMMITTED"
                       )

SQLALCHEMY_POOL_RECYCLE = 10
SQLALCHEMY_POOL_TIMEOUT = 10

Base = declarative_base()

# 创建session
DbSession = sessionmaker(bind=engine)


# session = scoped_session(DbSession)
# session = DbSession()


class CUdr:

    def __init__(self):
        pass

    @classmethod
    def insert(cls, emps):
        '''
        emps = Store_score(
            store_id=store_id,
            class . column = val
        )
        '''
        session = DbSession()
        try:
            session.add(emps)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False

        finally:
            session.close()

    @classmethod
    def delete_real(cls, filter):
        session = DbSession()
        try:
            res = session.query(cls)
            for x in filter:
                res = res.filter(x)

            res.delete()
            session.commit()
            return True
        except:
            session.rollback()
            return False

        finally:
            session.close()

    @classmethod
    def delete(cls, filter):
        session = DbSession()
        try:
            res = session.query(cls)
            for x in filter:
                res = res.filter(x)
            update = {
                'is_use': 0
            }
            res.update(update)
            session.commit()
            return True
        except:
            session.rollback()
            return False

        finally:
            session.close()

    @classmethod
    def update(cls, filter, update: dict):
        '''
        :param filter: 查询条件
        :param update: 更改内容
        :return:
        :ex.
                update = {
                    'nick_name': nick_name,
                    'phone': phone
                }
                filter = {User.id == id}
        '''
        session = DbSession()
        try:
            res = session.query(cls)
            for x in filter:
                res = res.filter(x)
            # res = res.filter(filter)
            num = res.update(update)
            session.commit()
            return True, num
        except:
            session.rollback()
            return False

        finally:
            session.close()

    @classmethod
    def __other_info(cls, session):
        # 耗时40ms
        res = session.query(cls).all()
        res = len(res)
        return res

    @classmethod
    def fetch_all(cls, session=None, limit=False, group=False, order: tuple = False, filter=False, group_concat=False):
        """
        :param session: 数据库会话
        :param limit: 分页 False / (页码，每页条目) (page,limit)
        :param group: 分组 False / 字段名
        :param order: 排序 False / (字段名,是否反向)
        :param filter: 过滤 False / {table.column <condition> value}
        :param group_concat: 多条件分组？
        :return: {
            "list": <data>,数据
            "list_length": len(res),本次查询长度
            "total_count": count,符合本次查询所有数据长度
            "last_page": last_page ，是否具有下一页
        }
        """
        last_page = 'no limit'
        count = "no count"

        res = session.query(cls)
        if group_concat:
            res = session.query(cls, group_concat)
        if filter:
            for x in filter:
                res = res.filter(x)
        if group:
            res = res.group_by(group)
        if order:
            if order[1]:
                res = res.order_by(order[0].desc())
            else:
                res = res.order_by(order[0])
        if limit:
            start = (limit[0] - 1) * limit[1]
            stop = limit[0] * limit[1]
            res = res.slice(start, stop)
            count = cls.__other_info(session)

        try:
            res = res.all()
        except:
            session.rollback()
            res = res.all()

        if limit:
            res_len = len(res)
            last_page = False
            if res_len < limit[1]:
                last_page = True

        # session.flush()
        a = []
        for x in res:
            x = cls.to_dict(x)
            a.append(x)
        # if  counts =
        # count = cls.__other_info(session)
        # count = ""
        result = {
            "list": a,
            "list_length": len(res),
            "total_count": count,
            "last_page": last_page
        }
        # session.close()
        return result

    @classmethod
    def fetch_one(cls, session=None, filter=False, **column):
        """
        :param session: 本次会话
        :param filter: 过滤器
        :param column: 其他 已弃用
        :return: {clounm：value}
        """
        session_flag = False
        if session is None:
            session_flag = True
            session = DbSession()

        res = session.query(cls)

        # if column:
        #     t = []
        #     for xt in column:
        #         t.append(column[xt])
        #     res = session.query(*t)

        if filter:
            for x in filter:
                res = res.filter(x)
        try:
            res = res.first()
        except Exception as e:
            session.rollback()
            res = res.first()
            session.flush()
        res = cls.to_dict(res)

        # if session is None:
        # session.close()
        if session_flag:
            session.close()
        return res

    def __repr__(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]

        return json.dumps(fields, cls=DateEncoder, ensure_ascii=False)

    @classmethod
    def to_dict(cls, obj):
        # 数据改字典 对象形式
        if obj is None:
            return None
        d = dict()
        for c in cls.__table__.columns:
            try:
                # 统一处理时间
                v = getattr(obj, c.name)
                if c.name == "create_time" or c.name == 'update_time' or c.name == 'nickname_time':
                    try:
                        v = v.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        pass
                if c.name == 'password':
                    v = '我是加密字符串'
                host_domain = upload_host()
                if c.name == 'avatar_url':
                    v = host_domain + v + "?sukiyou=" + str(int(time.time()))
                if c.name == 'avatarurl':
                    v = host_domain + v + "?sukiyou=" + str(int(time.time()))

                if c.name == 'price':
                    v = '{:.2f}'.format(v / 100)

                if c.name == 'image_url':
                    v = host_domain + v + "?sukiyou=" + str(int(time.time()))
                d[c.name] = v
            except:
                v = None

        return d


# 处理json格式化时 时间问题
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)
