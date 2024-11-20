import jwt
import uuid
from logindemo import settings
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import algorithms
from Crypto.Cipher import AES
from binascii import b2a_base64, a2b_base64
import math
import urllib.parse
import datetime

MODE = AES.MODE_CBC


# jwt创建token
def create_jwttoken(payload):
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=30)  # 超时时间, 不写默认不过期
    payload["jti"] = str(uuid.uuid4())
    slat = settings.SECRET_KEY
    headers = {
        'type': 'jwt',
        'alg': 'HS256'
    }
    jwt_token = jwt.encode(payload=payload, key=slat, algorithm='HS256', headers=headers)
    return jwt_token


# 解析jwttoken
def analysis_jwttoken(token):
    salt = settings.SECRET_KEY
    payload = {}
    try:
        payload = jwt.decode(jwt=token, key=salt, algorithms=['HS256'])
        success, message = True, "token正常"
    except jwt.ExpiredSignatureError:
        success, message = False, "token已失效"
    except jwt.DecodeError:
        success, message = False, "token认证失败"
    except jwt.InvalidTokenError:
        success, message = False, "非法token"
    except Exception as e:
        success, message = False, e

    return {'status': success, 'msg': message, 'payload': payload}