# -*- coding:utf-8 -*-
import json
import time
from urllib.parse import urljoin

import feedparser
import requests
from lxml import etree
from termcolor import cprint
import schedule


class FeiShuBot:
    # 初始化webhook地址
    def __init__(self):
        self.webhook_url = ''
        self.morning_time = time.strftime("%a, %d %b %Y", time.localtime())
        self.evening_time = time.strftime('%Y-%m-%d', time.localtime())
        # 设置早报推送时间
        self.morning_page_time = '08:00'
        # 设置晚报推送时间
        self.evening_page_time = '16:00'
    
    # 推送消息到飞书
    def send(self, data):
        resp = requests.post(url=self.webhook_url, data=json.dumps(data))
        # {'StatusCode': 0, 'StatusMessage': 'success', 'code': 0, 'data': {}, 'msg': 'success'}
        if resp.json()['StatusCode'] == 0 and resp.json()['StatusMessage'] == 'success':
            self.output('[*]:消息发送成功!')
    
    # 推送文本消息
    def send_text(self, msg):
        data = {
            "msg_type": "text",
            "content": {
                "text": f"{msg}"
            }
        }
        self.send(data=data)
    
    # 定义消息输出
    def output(self, msg):
        if "error" in msg or "ERROR" in msg:
            color = "red"
        elif '[*]' in msg:
            color = "cyan"
        elif '[+]' in msg:
            color = 'yellow'
        else:
            color = "magenta"
        time_now = time.strftime("%Y-%m-%d %X")
        cprint(f"[{time_now}]:{msg}", color)
    
    # 获取早报信息
    def get_morning_page(self):
        titles = []
        hrefs = []
        try:
            rs1 = feedparser.parse('https://www.freebuf.com/feed')
            for ent in rs1['entries']:
                if self.morning_time in ent['published']:
                    titles.append(ent['title'])
                    hrefs.append(ent['link'])
        except Exception as e:
            self.output("ERROR：获取FreeBuf早报出错，错误信息： {}".format(e))
        
        if titles and hrefs:
            self.send_safety_msg('FreeBuf早报', titles, hrefs, '   点击查看!')
    
    # 获取晚报信息
    def get_evening_page(self):
        titles = []
        hrefs = []
        # 获取先知社区文章
        try:
            rs1 = feedparser.parse('https://xz.aliyun.com/feed')
            for ent in rs1['entries']:
                if self.evening_time in ent['published']:
                    titles.append(ent['title'])
                    hrefs.append(ent['link'])
        except Exception as e:
            self.output("ERROR：获取先知社区文章错误，错误信息：{}".format(e))
        
        # 获取奇安信攻防社区文章
        try:
            rs2 = feedparser.parse('https://forum.butian.net/Rss')
            for ent1 in rs2['entries']:
                if self.evening_time in ent1['published']:
                    titles.append(ent1['title'])
                    hrefs.append(ent1['link'])
        except Exception as e:
            self.output('ERROR：获取奇安信攻防社区文章错误，错误信息：{}'.format(e))
        
        # 获取安全客文章
        aqk_url = 'https://www.anquanke.com/knowledge'
        try:
            resp = requests.get(url=aqk_url)
            tree = etree.HTML(resp.text)
            div_list = tree.xpath('//*[@id="post-list"]/div')
            for div in div_list:
                title = div.xpath('.//div[@class="title"]/a/text()')
                href = div.xpath('.//div[@class="title"]/a/@href')
                port_time = div.xpath('.//div[@class="info"]/div/span/span/text()')
                print(port_time)
                # 进一步处理数据
                if title:
                    title = title[0].strip()
                    href = urljoin(aqk_url, href[0].strip())
                    port_time = port_time[1].strip()
                    if self.evening_time in port_time:
                        titles.append(title)
                        hrefs.append(href)
        except Exception as e:
            self.output('ERROR：获取安全客文章错误，错误信息：{}'.format(e))
        if titles and hrefs:
            self.send_safety_msg('安全晚报', titles, hrefs, '  点击查看!')
    
    # 推送安全咨询
    def send_safety_msg(self, title, child_titles, child_hrefs, a_content):
        msg_list = []
        for child_title, child_href in zip(child_titles, child_hrefs):
            content = [{
                'tag': 'text',
                'text': child_title,
            },
                {
                    "tag": "a",
                    "text": f"{a_content}\t\n",
                    "href": f"{child_href}\t\n"
                }]
            msg_list.append(content)
        
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"{title}",
                        "content": msg_list
                    }
                }
            }
        }
        
        self.send(data=data)
    
    def push_listen(self):
        self.send_text('链接成功!')
        schedule.every().day.at(self.morning_page_time).do(self.get_morning_page)
        schedule.every().day.at(self.evening_page_time).do(self.get_evening_page)
        while True:
            schedule.run_pending()


if __name__ == '__main__':
    Fsb = FeiShuBot()
    Fsb.push_listen()
