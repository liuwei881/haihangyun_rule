#coding=utf-8

from models import DB_Session, Article, Sensitive
import jieba
from smallgfw import GFW
import smtplib, datetime
from email.mime.text import MIMEText
from langconv import *

session = DB_Session()
with open("mingan.txt", "rb") as mingan:
	ciku = mingan.readlines()
ciku = map(lambda f: f.strip("\n").decode("utf-8"), ciku)
gfw = GFW()
gfw.set(ciku)
all_result = session.query(Article).all()

def send_main(all_result):
	'''将list for 改成yield方式'''
	for i in all_result:
		yield i

for i in send_main(all_result):
	try:
		line = Converter('zh-hans').convert(i.body)
	except UnicodeDecodeError:
		line = Converter('zh-hans').convert(i.body.decode('utf-8'))
	seg_list = jieba.cut(line, cut_all=False) #精确匹配模式
	seg_list = ",".join(seg_list)
	if gfw.check(seg_list):
		msg = MIMEText("url: {0} 有敏感字异常，请及时处理".format(i.url))
		send_from = "13810439560@163.com"
		send_to = "liuwei@polex.com.cn"
		msg['Subject'] = "海航云监控敏感词邮件"
		msg['From'] = send_from
		msg['To'] = send_to
		s = smtplib.SMTP('localhost')
		s.sendmail(send_from, send_to, msg.as_string())
		s.quit()
		session = DB_Session()
		word = Sensitive(url=i.url, sensitive_word=",".join([i[2] for i in gfw.check(seg_list)]), insert_time=datetime.datetime.now())
		session.add(word)
		session.commit()
		session.close()
	else:
		print 'ok'