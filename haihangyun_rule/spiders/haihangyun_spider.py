#coding=utf-8

from utils import parse_text
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from items import HaiHangYunRuleItem
from bs4 import BeautifulSoup

class HaiHangYunSpider(CrawlSpider):
    #name = "haihangyun"

    def __init__(self, rule):
        self.rule = rule
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []
        # 添加抽取文章链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow=[rule.allow_url],
            restrict_xpaths=[rule.extract_from]),
            callback='parse_item', follow=True))
        self.rules = tuple(rule_list)
        super(HaiHangYunSpider, self).__init__()

    def parse_item(self, response):
        data = response.body
        soup = BeautifulSoup(data, "lxml")
        sites = soup.find_all('p')
        article = HaiHangYunRuleItem()
        article["url"] = response.url
        article["title"] = soup.find_all("title")[0]
        article["body"] = "".join([i.text for i in sites])
        yield article