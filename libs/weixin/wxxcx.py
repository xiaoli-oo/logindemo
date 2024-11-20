import requests


class WeChatXCXLogin(object):

    def __init__(self, appid, secret):
        self.access_token = None
        self.refresh_token = None
        self.session_key = None
        self.appid = appid
        self.secret = secret
        self.get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'
        self.get_phone_number_url = 'https://api.weixin.qq.com/wxa/business/getuserphonenumber'
        self.code2_session_url = 'https://api.weixin.qq.com/sns/jscode2session'
        self.check_encrypted_data_url = "https://api.weixin.qq.com/wxa/business/checkencryptedmsg"

    # 获取access token
    def getAccessToken(self):
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.secret
        }
        page = requests.get(url=self.get_access_token_url, params=params)
        result = page.json()
        # print (result)
        if not result.get('access_token'):
            print(result.get('errmsg'))
            return False, result.get('errmsg')
        else:
            return True, result

    # 微信小程序授权获取手机号
    def getPhoneNumber(self, js_code, access_token=None):
        if not access_token:
            code, result = self.getAccessToken()
            if not code:
                return False, result
            access_token = result.get('access_token')

        data = {
            'access_token': access_token,
            'code': js_code
        }
        page = requests.post(
            url=self.get_phone_number_url + "?access_token={0}".format(access_token),
            data=data
        )
        result = page.json()
        # print (result)

        if str(result.get('errcode')) != '0':
            return False, result.get('errmsg')
        else:
            return True, result.get('phone_info')

    def code2Session(self, js_code):
        params = {
            "appid": self.appid,
            "secret": self.secret,
            "grant_type": "authorization_code",
            "js_code": js_code,
        }
        page = requests.get(url=self.code2_session_url, params=params)
        result = page.json()
        # print (result)
        """
        openid	string	用户唯一标识
        session_key	string	会话密钥
        unionid	string	用户在开放平台的唯一标识符，若当前小程序已绑定到微信开放平台帐号下会返回，详见 UnionID 机制说明。
        errcode	number	错误码
        errmsg	string	错误信息
        """
        if not result.get('openid'):
            print(result.get('errmsg'))
            return False, result.get('errmsg')
        else:
            return True, result

    # 检查加密信息是否由微信生成
    def checkEncryptedData(self, encrypted_msg_hash, access_token=None):
        if not access_token:
            code, result = self.getAccessToken()
            if not code:
                return False, result
            access_token = result.get('access_token')

        data = {
            'access_token': access_token,
            'encrypted_msg_hash': encrypted_msg_hash
        }
        page = requests.post(
            url=self.check_encrypted_data_url + "?access_token={0}".format(access_token),
            data=data
        )
        result = page.json()
        # print (result)

        if str(result.get('errcode')) != '0':
            return False, result.get('errmsg')
        else:
            return True, {'vaild': result.get('vaild'), 'created_at': result.get('created_at')}
