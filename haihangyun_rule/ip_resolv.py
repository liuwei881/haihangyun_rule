#coding=utf-8

import json, urllib, requests, random
from models import DB_Session, HaiHangYunRule
import nmap, redis

#通过扫描获取IP地址，然后通过IP地址获取域名
#ip_list为一个ip list的例子

ip_list = ['42.62.25.143', '220.181.90.8']
domain_list = []
fip_list = []
def get_domain(func):
	'''获取域名的list'''
	global domain_list
	global fip_list
	for ip in ip_list:
		result = json.loads(func(ip))
		if result["status"] == "Fail" or result["domainCount"] == '0':
			fip_list.append(ip)
		elif 'domainArray' in result:
			domain_list = [x[0] for x in result['domainArray'] if all(s not in x[0] for s in ("gov", "edu", "org"))]
			domain_list = map(lambda f:f.encode('utf-8'), list(set(domain_list)))
	return domain_list

@get_domain
def send(ip):
	'''从接口获取response的text'''

	url = 'http://domains.yougetsignal.com/domains.php'
	data = urllib.urlencode({'remoteAddress': ip})
	user_agent_list = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
					'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
					'Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.16',
					'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1']
	headers = {
        "User-Agent": "{0}".format(random.choice(user_agent_list)),
        "Host": "domains.yougetsignal.com",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
	}
	response = requests.post(url, params=data, headers=headers)
	return response.text

#对域名进行处理
domain_list = map(lambda f: ".".join(f.split(".")[1:]), domain_list)
domain_list.extend(filter(lambda f: len(f.split(".")) == 2, domain_list))
[domain_list.pop(domain_list.index(i)) for i in domain_list if "." not in i]

Redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=1)

#将域名插入数据库
db = DB_Session()
nm = nmap.PortScanner()
#要扫描的ip插入数据库
ports = []
if fip_list:
	for i in fip_list:
		protocol_dict = nm.scan(i, '1-65535')['scan'][i]['tcp']
		ports = [k for k,v in protocol_dict.iteritems() if v['name'] == 'http']
		if ports:
			for j in ports:
				if Redis.exists('url:%s' % 'http://{0}'.format(i) + ':{0}'.format(j)):
					pass
				else:
					Redis.set('url:%s' % 'http://{0}'.format(i) + ':{0}'.format(j), 1)
					ip_insert = HaiHangYunRule(name=i, allow_domains=i,
						start_urls='http://{0}'.format(i) + ':{0}'.format(j),
						allow_url='/',
						extract_from='//div',
						enable=1)
					db.add(ip_insert)
					db.commit()

#将域名批量插入数据库
db.execute(
	HaiHangYunRule.__table__.insert(),
    [{'name': i.split(".")[1],
	  'allow_domains': i.split(".")[1:],
	  'start_urls': 'http://{0}'.format(i),
	  'allow_url': '/',
	  'extract_from':'//div',
	  'enable': 1} for i in domain_list]
)
db.commit()