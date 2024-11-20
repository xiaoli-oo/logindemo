from logindemo import config_ali, config
import oss2
from libs import utils
import hashlib
import uuid
import time


class OssServer():
    def __init__(self, bucker_name=None):
        self.oss_access_key = config_ali.AccessKeyId
        self.oss_access_secret = config_ali.AccessKeySecret
        auth = oss2.Auth(self.oss_access_key, self.oss_access_secret)
        self.bucket_name = bucker_name or config_ali.BUCKER_NAME
        if config.DEBUG:
            self.end_point = config_ali.END_POINT
        else:
            self.end_point = config_ali.INTERNAL_END_POINT
        self.bucket = oss2.Bucket(auth, self.end_point, self.bucket_name, connect_timeout=30)

    # 上传网络流文件&内容文件
    def upload_file(self, dir, fileurl, ossfilepath=None):
        if not ossfilepath:
            ossfilepath = dir + "/" + str(uuid.uuid1()).replace('-', '')
        # self.bucket.put_object(ossfilepath, fileurl)
        return self.bucket.put_object(ossfilepath, fileurl)

    # 简单上传
    def upload_loaclfile(self, dir, filepath, ossfilepath=None):
        if not ossfilepath:
            ossfilepath = dir + "/" + str(uuid.uuid1()).replace('-', '')
        # self.bucket.put_object_from_file(ossfilepath, filepath)
        return self.bucket.put_object_from_file(ossfilepath, filepath)

    # 获取含有有效期签名的文件url
    def get_file_url(self, ossfilepath):
        file_url = self.bucket.sign_url("GET", ossfilepath, 3600)
        return file_url

    # 删除文件
    def delete_file(self, ossfilepath):
        self.bucket.delete_object(ossfilepath)
