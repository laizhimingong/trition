import requests
import sys
import os
import json
import logging
import time,datetime

# logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s, %(filename)s, %(levelname)s, %(message)s',
#              datefmt = '%a, %d %b %Y %H:%M:%S',
#              filename = os.path.join('/tmp','weixin.log'),
#              filemode = 'a')

corpid='ww7f2be677b461ce33'
appsecret='6jIqrtF3OPa41I89K1XFUwWkpebhXnxs4qcX74m5mK8'
agentid=1000003
#»ñÈ¡accesstoken
# token_url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret
# req=requests.get(token_url)
# accesstoken=req.json()['access_token']

def gettoken(*agr,**kwargs):
    corpid = 'ww7f2be677b461ce33'
    appsecret = '6jIqrtF3OPa41I89K1XFUwWkpebhXnxs4qcX74m5mK8'
    token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret
    req = requests.get(token_url)
    accesstoken = req.json()['access_token']
    print(accesstoken)
    return accesstoken
def get_userid(*agr,**kwargs):
    accesstoken = gettoken()
    #获取部门userid
    req = requests.get('https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token='+accesstoken+'&department_id=1&fetch_child=1', timeout=30)
    req_jason = req.json()
    userlist = req_jason.get('userlist')
    print(userlist)
    users=[]
    for user in userlist:
        users.append(user.get('userid'))
        print(user.get('userid'))
    print(users)
    return users
def push_message(*agr,**kwargs):
    agentid = 1000003
    # users=get_userid()
    # print(users)
    accesstoken = gettoken()
    msgsend_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken
    num=0
    users=['Cheng-Loto', 'enovoa', 'shaoshuao', 'zhuke', 'KongDeJun', 'LiuZaiTian', 'ChangTao']
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    start_time2 = datetime.datetime.now()
    print(start_time)
    for user in range(0, 10):
        for item in  range(0,len(users)):
            touser = users[item]
            message = 'joke暴力推送告警测试中............,请屏蔽'
            params = {
                "touser": touser,
                #       "toparty": toparty,
                "msgtype": "text",
                "agentid": agentid,
                "text": {
                    "content": message
                },
                "safe": 0
            }
            req = requests.post(msgsend_url, data=json.dumps(params))
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    end_time2 = datetime.datetime.now()
    caltime = (end_time2 - start_time2).seconds
    print(end_time)
    print(caltime)
    # while num < 101:
    #     for user in range(0,len(users)):
    #         touser = 'shaoshuao'
    #         message = 'joke暴力推送告警测试中............,请屏蔽'
    #         params = {
    #             "touser": touser,
    #             #       "toparty": toparty,
    #             "msgtype": "text",
    #             "agentid": agentid,
    #             "text": {
    #                 "content": message
    #             },
    #             "safe": 0
    #         }
    #         req = requests.post(msgsend_url, data=json.dumps(params))
    #     num = num + 1
    #     print(num)




push_message()
# logging.info('sendto:' + touser + ';;subject:' + subject + ';;message:' + message)