import time
import uuid
import jwt
from logindemo import settings
import datetime

def create_token():
    slat = settings.SECRET_KEY
    headers = {
        'type': 'jwt',
        'alg': 'HS256'
    }
    # 构造payload exp务必选择UTC时间
    payload = {
        'uid': 1, # 自定义用户ID
        'username': 'xiaoli',
        'client_type': 'web', # 自定义用户名
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1), # 过期时间
        # "ss":"签发人",
        # "iat":"签发时间",
        # "sub":"主题",
        # "aud":"受众",
        # "nbf":"生效时间",
        "jti": str(uuid.uuid1())
    }
    token = jwt.encode(payload=payload, key=slat, algorithm='HS256', headers=headers).decode()
    print(token)
    return token


def analysis_token(token):
    salt = settings.SECRET_KEY
    try:
        payload = jwt.decode(jwt=token, key=salt, algorithms=['HS256'])
        print(payload)
        print(type(payload))
    except jwt.ExpiredSignatureError as e:
        print (e)
        print({"success": False, "message": "token已失效"})
    except jwt.DecodeError:
        print({"success": False, "message": "token认证失败"})
    except jwt.InvalidTokenError:
        print({"success": False, "message": "非法token"})


token = create_token()
# time.sleep(5)
token = create_token()
time.sleep(5)
analysis_token(token)