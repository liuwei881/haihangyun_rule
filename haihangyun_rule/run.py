#coding=utf-8

import logging
from spiders.haihangyun_spider import HaiHangYunSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from models import HaiHangYunRule
from models import DB_Session

if __name__ == '__main__':
    db = DB_Session()
    settings = get_project_settings()
    rules = db.query(HaiHangYunRule).filter(HaiHangYunRule.enable == 1).all()
    db.close()
    runner = CrawlerRunner(settings)

    for rule in rules:
        runner.crawl(HaiHangYunSpider, rule=rule)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    # blocks process so always keep as the last statement
    reactor.run()
    logging.info('all finished.')