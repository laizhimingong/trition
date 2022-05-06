import json
from django.http import HttpResponse
import requests


# 发送私人微信告警信息
def sendWechat02(content):
    print("sendWechat02")
    url = "https://wechat.xiaocaicai.com/send_message"
    headers = {'content-type': 'application/json'}
    data = {
        "userid": "20289907708@chatroom",
        "message": content
    }
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    return res.text


# 发送微信告警(企业微信测试中)
def sendWechat01(message):
    print("sendWechat01")
    # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ea2353a4-00c8-4f20-b6a9-b27c89c2f81d"
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7034c2e2-de6d-4fe2-8bf6-e242cdd5dcae"
    headers = {"Content-Type": "text/plain"}
    data = {
        "msgtype": "text",
        "text": {
            "content": message,
        }
    }
    ret = requests.post(url=url, headers=headers, data=json.dumps(data))
    return ret

def sendWechat03(message):
    print("sendWechat03")
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
    print(ret)
    return ret
if __name__ == '__main__':
    status_color = 'info'
    senddata = '''<font color=warning>报警</font> - **磁盘使用率已超85%**
    ><font color="comment">级别:Warning</font>
    ><font color="comment">发生:2021-07-12 01:29:00</font>
    ><font color="comment">持续:68 days, 1:10:32</font>
    ><font color="comment">详情:Instance 172.20.0.113 当前: /data DISK usage值: 90% > 85%.</font>
    >
    ><font color="comment">实例:172.20.0.113</font>
    ><font color="comment">环境:PRD</font>
    ><font color="comment">机房:IDC</font>
    ><font color="comment">业务:大数据平台</font>
    ><font color="comment">报警:2021-09-18 02:39:32</font>'''
    # sendWechat01(senddata)
    # sendWechat02(senddata)
    sendWechat03(senddata)
