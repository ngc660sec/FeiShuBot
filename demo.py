# -*- coding:utf-8 -*-
import json
import requests


class FeiShuDemo:
    def __init__(self):
        self.webhook_url = ''
    
    # 发送消息至飞书
    def send_msg(self, data):
        """
        :param data: 构建的data数据
        :return:
        """
        resp = requests.post(url=self.webhook_url, data=json.dumps(data))
        # 返回数据格式
        # {'StatusCode': 0, 'StatusMessage': 'success', 'code': 0, 'data': {}, 'msg': 'success'}
        if resp.json()['StatusCode'] == 0 and resp.json()['StatusMessage'] == 'success':
            print('消息发送成功!')
    
    # 发送文本消息
    def send_text(self, msg):
        """
        :param msg: 发送消息文本
        :return:
        """
        data = {
            "msg_type": "text",
            "content": {
                "text": f"{msg}"
            }
        }
        self.send_msg(data=data)
    
    # 发送富文本消息
    def send_post(self, title_msg, text_msg, a_text, a_href):
        """
        :param title_msg:   标题信息
        :param text_msg:    文本信息
        :param a_text:      链接文本
        :param a_href:      链接地址
        :return:
        """
        data = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"{title_msg}",
                        "content": [
                            [{
                                "tag": "text",
                                "text": f"{text_msg}: "
                            },
                                {
                                    "tag": "a",
                                    "text": f"{a_text}",
                                    "href": f"{a_href}"
                                },
                            ],
                            [
                                {
                                    'tag': 'text',
                                    'text': '第二行: ',
                                },
                                {
                                    'tag' : 'a',
                                    'text': '点击有惊喜',
                                    'href': 'http://baidu.com'
                                }

                            ]
                        ]
                    }
                }
            }
        }
        self.send_msg(data=data)
    
    # 发送消息卡片
    def send_card(self, title_msg, text_msg, button_msg, button_href):
        """
        :param title_msg:   标题
        :param text_msg:    文本消息
        :param button_msg:  按钮文本
        :param button_href: 按钮跳转链接
        :return:
        """
        data = {
            "msg_type": "interactive",
            "card": {
                "elements": [{
                    "tag": "div",
                    "text": {
                        "content": f"{text_msg}",
                        "tag": "lark_md"
                    }
                }, {
                    "actions": [{
                        "tag": "button",
                        "text": {
                            "content": f"{button_msg} :玫瑰:",
                            "tag": "lark_md"
                        },
                        "url": f"{button_href}",
                        "type": "default",
                        "value": {}
                    }],
                    "tag": "action"
                }],
                "header": {
                    "title": {
                        "content": f"{title_msg}",
                        "tag": "plain_text"
                    }
                }
            }
        }
        self.send_msg(data=data)
    
    def run(self):
        # self.send_text(msg='测试')
        self.send_post('官网更新提醒', '官网更新了', '点击查看', 'http://ngc660.cn')
        # self.send_card('NGC660安全实验室好牛', '**NGC660安全实验室**，致力于网络安全攻防、WEB渗透、内网渗透、代码审计、CTF比赛、红蓝对抗应急响应、安全架构等技术干货。性痴则其志凝，故书痴者文必工，艺痴者技必良。', button_msg='点击查看更多', button_href='http://ngc660.com')

if __name__ == '__main__':
    Fsd = FeiShuDemo()
    Fsd.run()
