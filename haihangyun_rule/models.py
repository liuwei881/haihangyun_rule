#coding=utf-8

import datetime

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from settings import DATABASE
from sqlalchemy.orm import sessionmaker



def db_connect():
    '''链接数据库'''
    return create_engine(URL(**DATABASE))


def create_news_table(engine):
    '''自动创建新表'''
    Base.metadata.create_all(engine)

def _get_date():
    '''获取当前日期'''
    return datetime.datetime.now()

DB_Session = sessionmaker(bind=db_connect())
Base = declarative_base()


class HaiHangYunRule(Base):
    '''自定义文章爬取规则'''
    __tablename__ = 'haihangyun_rule'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))                   # 规则名称
    allow_domains = Column(String(100))         # 运行的域名列表，逗号隔开
    start_urls = Column(String(100))            # 开始URL列表，逗号隔开
    allow_url = Column(String(100))             # 文章链接正则表达式(子串)
    extract_from = Column(String(100))          # 文章链接提取区域xpath
    enable = Column(Integer)                    # 规则是否生效


class Article(Base):
    '''爬取的内容类'''
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    url = Column(String(256))                   # 内容url
    title = Column(String(256))                 # 网页标题
    body = Column(Text)                         # 内容body
    insert_time = Column(DateTime, default=datetime.datetime.now())  # 插入时间

class Sensitive(Base):
    '''敏感词表'''
    __tablename__ = 'sensitive'

    id = Column(Integer, primary_key=True)
    url = Column(String(100))                   # 包含敏感词的url
    sensitive_word = Column(String(100))        # 敏感词
    insert_time = Column(DateTime, default=datetime.datetime.now())  # 插入时间

