内容监控系统分为三个组件：分别是：
1.http端口扫描url入库
调用Neutron的floating list接口，获取当前已被用户使用的公网IP地址。  
获取要爬取的IP/域名list。
根据ip的list，通过http://domains.yougetsignal.com/domains.php 提供的接口,获取域名的list，没有域名的获取直接获取ip list。
使用redis 去重ip:端口的形式。
将扫描的结果 ip形式的一个一个插入数据库(由于端口不同，批量无法插入)。
域名形式的批量插入数据库(数据库表结构，后面给出)。
 
2.爬取-存储
  使用scrapy爬取相关页面.(分布式可以使用redis queue )
  每5秒钟爬取一次，为了防止被ban。
  获取: 1、页面的标题，2、页面的内容, 3、页面的url。
  使用redis去重，将有问题的页面存入MySql，内容有变化即入库。
3.关键字过滤
 从MySql读取页面内容。
 使用DFA算法对页面内容进行敏感字过滤。有敏感字词库(根据需要自己添加敏感字)。
 将有问题的url，以邮件的形式发送给指定人。

4.MySql表结构
数据库名 spider.
| articles | CREATE TABLE `articles` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`url` varchar(255) DEFAULT NULL,
`title` varchar(255) DEFAULT NULL,
`body` text,
`insert_time` datetime DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8 |
haihangyun_rule | CREATE TABLE `haihangyun_rule` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(255) DEFAULT NULL,
`allow_domains` varchar(100) DEFAULT NULL,
`start_urls` varchar(100) DEFAULT NULL,
`allow_url` varchar(200) DEFAULT NULL,
`extract_from` varchar(200) DEFAULT NULL,
`enable` smallint(2) DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 |
sensitive | CREATE TABLE `sensitive` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`url` varchar(100) DEFAULT NULL,
`sensitive_word` varchar(100) DEFAULT NULL,
`insert_time` datetime DEFAULT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 |
5.MySql表说明
articles
url: 所爬取的url，
title: 所爬取的标题，
body: 所爬取的内容,
insert_time: 爬取的时间.
haihangyun_rule
name: 爬取的名称，
allow_domains: 允许爬取的域名，
start_urls: 开始爬取的url，
allow_url: 允许爬取的url，
extract_from: 文章链接提取区域xpath,
enable: 是否启动(0,不启用. 1,启用.)
sensitive
url: 有问题的url，
sensitive_word: 敏感词，
insert_time: 插入时间.
