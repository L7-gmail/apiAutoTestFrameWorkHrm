import base64
import hashlib
import hmac
import time
import urllib.parse

import requests

from config import setting
from config.setting import DINGDING_SECRET, DINGDING_WEBHOOK


def generate_sign():
    """
    生成加签计算
    :return:
    """
    # 获取当前时间的时间戳
    timestamp = str(round(time.time() * 1000))
    # 获取钉钉机器人里面的加签秘钥
    secret = DINGDING_SECRET
    # 转码成utf-8
    secret_enc = secret.encode('utf-8')
    # 组合当前时间戳和加签秘钥
    str_to_sign = f"{timestamp}\n{secret}"
    # 转成byte类型
    str_to_sign_enc = str_to_sign.encode('utf-8')
    # 通过加密方式加密当前时间戳和秘钥
    hmac_code = hmac.new(secret_enc, str_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    return timestamp, sign


def send_dd_msg(content_str, at_all=True):
    """
    向钉钉群发送消息
    :param content_str: 发送的内容
    :param at_all: @全员，默认为True
    :return:
    """
    timestamp, sign = generate_sign()
    # 组成一个完整的url地址
    url = f"{DINGDING_WEBHOOK}&timestamp={timestamp}&sign={sign}"
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data = {
        'msgtype': 'text',
        'text': {
            'content': content_str
        },
        'at': {
            'isAtAll': at_all
        }
    }

    res = requests.post(url=url, json=data, headers=headers)
    return res.text


if __name__ == '__main__':
    res_text = send_dd_msg("钉钉测试",at_all=False)
    print(res_text)