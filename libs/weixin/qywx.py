# 企业微信
import requests
import time


class QYWeiXin(object):

    def __init__(self, corpid, corpsecret, qy_agentid):
        self.access_token = None
        self.access_token_expires = 0
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.get_access_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        self.send_msg_url = ' https://qyapi.weixin.qq.com/cgi-bin/message/send'
        self.qy_agentid = qy_agentid

    # 获取access token
    def getAccessToken(self):
        if self.access_token and self.access_token_expires > time.time():
            return True, self.access_token

        params = {
            "corpid": self.corpid,
            "corpsecret": self.corpsecret
        }
        page = requests.get(url=self.get_access_token_url, params=params)
        result = page.json()
        if not result.get('access_token'):
            print(result.get('errmsg'))
            return False, result.get('errmsg')
        else:
            self.access_token = result.get('access_token')
            self.access_token_expires = int(time.time()) + int(result.get('expires_in'))
            return True, self.access_token

    def send_msg(self, touser, content):
        params = {
            'access_token': self.access_token
        }
        data = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.qy_agentid,
            "text": {
                "content": content
            },
            "safe": 0
        }

    def recv_msg(self):
        pass

    def sign(self, body):
        if isinstance(body, bytes):
            body = body.decode('UTF-8')
