#coding=utf-8

import redis
import logging
from scrapy.exceptions import DropItem
from models import Article
from models import DB_Session

Redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
_log = logging.getLogger(__name__)

class DuplicatesPipeline(object):
    '''Item去重复'''
    def process_item(self, item, spider):
        if Redis.exists('body:%s' % item['body']):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            Redis.set('body:%s' % item['body'], 1)
            return item

class ArticleDataBasePipeline(object):
    '''保存内容到数据库'''

    def __init__(self):
        self.session = DB_Session()

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def process_item(self, item, spider):
        a = Article(url=item["url"], title=item["title"].strip("<title></title>").encode("utf-8"),body=item["body"].encode("utf-8"))
        self.session.add(a)
        self.session.commit()
        self.session.close()
    def close_spider(self, spider):
        pass
