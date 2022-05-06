from wxpusher import WxPusher
import requests
import json
import time

appToken="6a1b72152f8c41778601ef6223e4b26f"
content="""----------------〔Alarm Info〕----------------
【状态】: 报警
【名称】:磁盘使用率已超85%
【级别】:Warning
【发生】:2021-07-12 01:29:00
【持续】:68 days, 1:10:32
【详情】:Instance 172.20.0.113 当前: /data DISK usage值: 90% > 85%.
----------------〔Basic Info〕----------------
【实例】:172.20.0.113
【环境】:PRD
【机房】:IDC
【业务】:大数据平台
【报警】:2021-09-18 02:39:32
--------------------------------------------------
"""
summary= "【异常】:磁盘使用率已超85%"
topic_id="24142145"
def pusher(*args,**kwargs):
    url = "http://pushplus.hxtrip.com/send"
    headers = {'content-type': 'application/json'}
    data = {
        "token": appToken,
        "content": content,
        "title":summary,
        "template": 'json',
        "topic":topic_id,
    }
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    return res.text
# WxPusher.query_message('<messageId>')
# WxPusher.create_qrcode('<extra>', '<validTime>', '<appToken>')
# WxPusher.query_user('<page>', '<page_size>', '<appToken>')
if __name__ == '__main__':
    while True:
        time.sleep(1)
        print(pusher())