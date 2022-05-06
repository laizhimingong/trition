import json

import requests
from celery import task
from django.http import JsonResponse


# 发送微信告警(企业微信测试中)

@task
def sendEnterpriseWechat(message):
    print(sendEnterpriseWechat)
    # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ea2353a4-00c8-4f20-b6a9-b27c89c2f81d"
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7034c2e2-de6d-4fe2-8bf6-e242cdd5dcae"
    headers = {"Content-Type": "text/plain"}
    data = {
        "msgtype": "markdown",
        "safe":1,
        "markdown": {
            "content": message,
        }
    }
    ret = requests.post(url=url, headers=headers, data=json.dumps(data))
    json_ret = ret.json()
    return JsonResponse(json_ret)

# 发送<豹警官>微信告警信息
@task
def sendWechat(content):
    url = "https://wechat.xiaocaicai.com/send_message"
    headers = {'content-type': 'application/json'}
    data = {
        "userid": "20289907708@chatroom",
        "message": content
    }
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    return res.text

