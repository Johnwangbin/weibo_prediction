#coding:utf-8
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import CHAR,Integer,String,VARCHAR
from contextlib import contextmanager

class User(object):
    pass

BaseModel=declarative_base()

class Relations(BaseModel):
    __tablename__ = "relations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    blogger = Column(Integer, index=True, nullable=False)
    follower = Column(Integer, nullable=False)

class FollowerRelations(BaseModel):
    __tablename__ = "follower_relations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    blogger  = Column(Integer, index=True, nullable=False)
    follower = Column(VARCHAR(408), nullable=False)

#, ForeignKey("weibo_profile.id")
class RepostRelations(BaseModel):
    __tablename__ = "repost_relations"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    weibo_id    = Column(VARCHAR(20), nullable=False)
    blogger_id  = Column(Integer, nullable=False)
    transfer_id = Column(Integer, nullable=False)
    time_length = Column(Integer, nullable=False)
    content     = Column(VARCHAR(100))
    # index       = Index("weibo_blogger_ix", "weibo_id", "blogger_id", unique=True)

class WeiboProfile(BaseModel):
    __tablename__ = "weibo_profile"
    id          = Column(VARCHAR(20), primary_key=True, nullable=False)
    blogger_id  = Column(Integer, nullable=False)
    start_time  = Column(DATETIME)
    content     = Column(VARCHAR(200))

engine = create_engine(
            "mysql://root:888@192.168.0.100:3306/trend_prediction2?charset=utf8")
metadata = MetaData(engine)

def init_db():
    BaseModel.metadata.create_all(engine)

init_db()

@contextmanager
def open_session():
    session = sessionmaker(engine)()
    try:
        yield session
    finally:
        session.close()