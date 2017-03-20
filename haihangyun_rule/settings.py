# -*- coding: utf-8 -*-

# Scrapy settings for haihangyun_rule project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
import logging

BOT_NAME = 'haihangyun_rule'

SPIDER_MODULES = ['haihangyun_rule.spiders']
NEWSPIDER_MODULE = 'haihangyun_rule.spiders'


ITEM_PIPELINES = {
    'haihangyun_rule.pipelines.DuplicatesPipeline': 1,
    'haihangyun_rule.pipelines.ArticleDataBasePipeline': 2,
}
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'haihangyun_rule.middlewares.RotateUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    # 这是爬虫中间件， 543是运行的优先级
    # 'coolscrapy.middlewares.UrlUniqueMiddleware': 543,
}
ROBOTSTXT_OBEY = True

# 几个反正被Ban的策略设置
DOWNLOAD_TIMEOUT = 20
DOWNLOAD_DELAY = 5
# 禁用Cookie
COOKIES_ENABLES = True

LOG_LEVEL = logging.INFO
LOG_STDOUT = True
LOG_FILE = "/tmp/spider.log"
LOG_FORMAT = "%(asctime)s [%(name)s] %(levelname)s: %(message)s"

DATABASE = {'drivername': 'mysql',
            'host': '127.0.0.1',
            'port': '3306',
            'username': 'root',
            'password': '123456',
            'database': 'spider',
            'query': {'charset': 'utf8'}}