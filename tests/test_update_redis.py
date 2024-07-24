from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from redis import Redis
import pytest
from sqlalchemy import create_engine, Column, Integer, String, event, MetaData, Table, ForeignKey



@pytest.fixture
def init_sql_session():
    # 初始化数据库引擎及会话
    engine = create_engine('mysql+pymysql://root:gungun@localhost:3306/test')  # 更换为您的数据库 URI
    
    metadata=MetaData(engine)
    # 定义一个ORM模型
    user=Table('user',metadata,
        Column('id',Integer,primary_key=True),
        Column('name',String(20)),
        Column('fullname',String(40)),
        )
    address_table = Table('address', metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', None, ForeignKey('user.id')),
        Column('email', String(128), nullable=False)
        )
    metadata.create_all()
    
    Session = sessionmaker(bind=engine)
    session = Session()
    # 初始化 Redis 连接
    redis_conn = Redis(host='localhost', port=6379, db=0)

    return session, redis_conn, user

# 您的缓存键生成函数
def make_cache_key(table_name, instance):
    """
    根据不同的缓存，给出不同的key
    eg: 基于查询的
        基于表和查询参数的

    """
    return f"{table_name}:{instance.id}"

def test_monitor_sql(init_sql_session):
    session, redis_conn, user = init_sql_session()

    # SQLAlchemy 事件监听器
    def after_update_listener(mapper, connection, target):
        # 删除与实例相关的 Redis 缓存
        cache_key = make_cache_key(target)
        redis_conn.delete(cache_key)

    # 将事件监听器附加到 SQLAlchemy 的 `after_update` 事件
    event.listen(user, 'after_update', after_update_listener)

    # 更新一个实体的示例
    with session.begin():
        instance = session.query(user).filter_by(id=1).first()
        print(instance)
        if instance:
            instance.name = 'gungun'
            session.add(instance)
        # 在此处不需要显式删除缓存，因为事件监听器会自动处理

    # 关闭会话
    session.close()