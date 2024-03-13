from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from redis import Redis
import pytest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, event

Base = declarative_base()
# 定义一个ORM模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)


@pytest.fixture
def init_sql_session():
    # 初始化数据库引擎及会话
    engine = create_engine('sqlite:///your_database.db')  # 更换为您的数据库 URI
    Session = sessionmaker(bind=engine)
    session = Session()
    # 初始化 Redis 连接
    redis_conn = Redis(host='localhost', port=6379, db=0)

    return session, redis_conn

# 您的缓存键生成函数
def make_cache_key(table_name, instance):
    """
    根据不同的缓存，给出不同的key
    eg: 基于查询的
        基于表和查询参数的

    """
    return f"{table_name}:{instance.id}"

def test_monitor_sql(init_sql_session):
    session, redis_conn = init_sql_session()

    # SQLAlchemy 事件监听器
    def after_update_listener(mapper, connection, target):
        # 删除与实例相关的 Redis 缓存
        cache_key = make_cache_key(target)
        redis_conn.delete(cache_key)

    # 将事件监听器附加到 SQLAlchemy 的 `after_update` 事件
    event.listen(User, 'after_update', after_update_listener)

    # 更新一个实体的示例
    with session.begin():
        instance = session.query(User).filter_by(id=1).first()
        if instance:
            instance.some_field = 'new value'
            session.add(instance)
        # 在此处不需要显式删除缓存，因为事件监听器会自动处理

    # 关闭会话
    session.close()