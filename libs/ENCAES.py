import base64
import json
from Crypto.Cipher import AES

pad = lambda s: s + chr(16 - len(s) % 16) * (16 - len(s) % 16)
unpad = lambda s: s[:-s[-1]]


def aes_CBC_Encrypt(data, key, iv):  # CBC模式的加密函数，data为明文，key为16字节密钥,iv为偏移量
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')  # CBC 模式下的偏移量
    data = pad(data)  # 补位
    data = data.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)  # 创建加密对象

    # encrypt AES加密  B64encode为base64转二进制编码
    result = base64.b64encode(aes.encrypt(data))
    return str(result, 'utf-8')  # 以字符串的形式返回


def aes_CBC_Decrypt(data, key, iv):  # CBC模式的解密函数，data为密文，key为16字节密钥
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)  # 创建解密对象

    # decrypt AES解密  B64decode为base64 转码
    result = aes.decrypt(base64.b64decode(data))
    result = unpad(result)  # 除去补16字节的多余字符
    return str(result, 'utf-8')  # 以字符串的形式返回


if __name__ == '__main__':
    # str_a = '{a:1,b:1}'
    # b = aes_ECB_Encrypt(str_a, key)
    # b1 = aes_ECB_Decrypt(b, key)

    import datetime

    utc_time_str = datetime.datetime.utcnow().replace(second=0, microsecond=0).strftime("%Y%m%d%H")
    print(utc_time_str)
    key = 'fA4Ty7AkbbER02' + utc_time_str
    iv = '0102030405060708'
    print(key)
    print(iv)
    c = aes_CBC_Encrypt('{code: "aaa"}', key, iv)
    print(c)
    # c = "T9FN0aPiD0fa79X0GPjj27MTD3H09eCt2pke5i1ouKuix3BfnZXo7tcQw6qPnmuNrpawydIAfLflywxKC9iEH7Ny0EioKhsYfA2oriS8GBinRsY/2IwfBMcwoz0kCQxtFYUjxcixoA9Q1P8omx1pHkpyFy/zxHuYI14wt5ZiKHK0I+DBMECbEgTdZqfhCyX4"
    c1 = aes_CBC_Decrypt(c, key, iv)
    print(c1)
