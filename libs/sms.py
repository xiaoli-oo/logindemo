# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from logindemo import config_ali
import uuid


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 必填，您的 AccessKey ID,
            access_key_id=access_key_id,
            # 必填，您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def main(phone: str, v_code: int, t_code: str) -> tuple[bool, str] | tuple[bool, Exception]:
        """ 初始化 Client，采用 AK&SK 鉴权访问的方式，此方式可能会存在泄漏风险，建议使用 STS
        方式。鉴权访问方式请参考：https://help.aliyun.com/document_detail/378659.html # 获取 AK
        链接：https://usercenter.console.aliyun.com
        """
        client = Sample.create_client(config_ali.AccessKeyId, config_ali.AccessKeySecret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=config_ali.SMS_SIGN_NAME,
            template_code=t_code,
            template_param=str({"code": v_code}),
            out_id=str(uuid.uuid1())
        )
        try:
            # 复制代码运行请自行打印 API 的返回值
            result = client.send_sms_with_options(send_sms_request, util_models.RuntimeOptions())
            print(result.body.message)
            return True, 'ok'
        except Exception as error:
            # 如有需要，请打印 error
            return False, error
            # UtilClient.assert_as_string()

    @staticmethod
    async def main_async(phone: str, v_code: int, t_code: str) -> tuple[bool, str] | tuple[bool, Exception]:
        """  # 初始化 Client，采用 AK&SK 鉴权访问的方式，此方式可能会存在泄漏风险，建议使用 STS
        方式。鉴权访问方式请参考：https://help.aliyun.com/document_detail/378659.html # 获取 AK
        链接：https://usercenter.console.aliyun.com
        """
        client = Sample.create_client(config_ali.AccessKeyId, config_ali.AccessKeySecret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=phone,
            sign_name=config_ali.SMS_SIGN_NAME,
            template_code=t_code,
            template_param=str({"code": v_code}),
            out_id=str(uuid.uuid1())
        )
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.send_sms_with_options_async(send_sms_request, util_models.RuntimeOptions())
            return True, 'ok'
        except Exception as error:
            # 如有需要，请打印 error
            return False, error
            # UtilClient.assert_as_string(error.message)


if __name__ == '__main__':
    print(Sample.main("18903860173", 888888, config_ali.SMS_CODE))
    # Sample.main_async("18903860173", 888888, config_ali.SMS_CODE)
