import datetime
import json
import time

import pytz
import requests
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import redis
# 导入models
from alert import models as alertmodels
from common import models as commonmodels
from user.views import check_login

#引入celery task
from .tasks import sendEnterpriseWechat,sendWechat
#引入缓存
from django.views.decorators.cache import cache_page

# Create your views here.
# UTCS time to timestamp 2016-07-31t16:00:00z
def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%SZ'):
    local_tz = pytz.timezone('Asia/Chongqing')
    local_format = "%Y-%m-%d %H:%M"
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    time_str = local_dt.strftime(local_format)
    return int(time.mktime(time.strptime(time_str, local_format)))

#执行时间装饰器
def completionTime(method):
   def caltime(*args, **kw):
       start = time.time()
       result = method(*args, **kw)
       end = time.time()
       print('%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, end - start))
       return result
   return caltime

# 发送微信告警(企业微信测试中)
# def sendWechat01(message):
#     # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ea2353a4-00c8-4"
#     url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7034c2e2-de6d-4fe2-8b"
#     headers = {"Content-Type": "text/plain"}
#     data = {
#         "msgtype": "text",
#         "text": {
#             "content": message,
#         }
#     }
#     ret = requests.post(url=url, headers=headers, data=json.dumps(data))
#     return HttpResponse(ret.json())

def pushInterface(message):
    pass

def sendWechat01(message):
    # url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ea2353a4-00c8-4f89c2f81d"
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=7034c2e2-de6d-4fecdd5dcae"
    headers = {"Content-Type": "text/plain"}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": message,
        }
    }
    ret = requests.post(url=url, headers=headers, data=json.dumps(data))
    return ret


# 发送私人微信告警信息
def sendWechat02(content):
    url = "https://wechat.xiaocaicai.com/send_message"
    headers = {'content-type': 'application/json'}
    data = {
        "userid": "20289908@chatroom",
        "message": content
    }
    res = requests.post(url=url, headers=headers, data=json.dumps(data))
    return res.text


def push_wechat_gettoken(*agr, **kwargs):
    corpid = 'ww7f2be6ce33'
    appsecret = '6jIqrtF3OPaFUwWkpebhXnxs4qcX74m5mK8'
    token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + corpid + '&corpsecret=' + appsecret
    req = requests.get(token_url)
    accesstoken = req.json()['access_token']
    print(accesstoken)
    return accesstoken

def push_wechat_get_userid(*agr, **kwargs):
    accesstoken = push_wechat_gettoken()
    # 获取部门userid
    req = requests.get(
        'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=' + accesstoken + '&department_id=1&fetch_child=1',
        timeout=30)
    req_jason = req.json()
    userlist = req_jason.get('userlist')
    users = []
    for user in userlist:
        users.append(user.get('userid'))
    return users

def push_wechat_push_message(message):
    agentid = 1000003
    # users=push_wechat_get_userid()
    users=['qq', 'e2', 'sha', 'uke', 'Koun', 'LiTan', 'Chan']
    print(users)
    accesstoken = push_wechat_gettoken()
    print(accesstoken)
    msgsend_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + accesstoken
    for item in range(0, len(users)):
        touser = users[item]
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
# alertmanager告警webhook接口
@csrf_exempt
def webhook(request):
    # print('webhook')
    if request.method == 'POST':
        try:
            request_data = request.body
            request_dict = json.loads(request_data.decode('utf-8'))
            alerts = request_dict['alerts']
            sendtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 发送时间
            for alert in alerts:
                # 获取告警信息 各字段信息
                alertname = alert['labels']['alertname']
                status = alert['status']
                severity = alert['labels']['severity']
                env = alert['labels']['env']
                idc = alert['labels']['idc']
                business = alert['labels']['business']
                instance = alert['labels']['instance']
                ip = alert['labels']['ip']
                port = alert['labels']['port']
                summary = alert['annotations']['summary']
                description = alert['annotations']['description']
                exporter = alert['labels']['exporter']
                fingerprint = alert['fingerprint']
                # 時間轉換
                startsAt = alert['startsAt'].split(".")[0] + 'Z'
                ret_startsAt = utc_to_local(startsAt)
                ltime_startsAt = time.localtime(ret_startsAt)
                startsAt = time.strftime("%Y-%m-%d %H:%M:%S", ltime_startsAt)  # 开始时间
                if alert['endsAt'][0:10] == "0001-01-01":
                    endsAt = ""
                    # 计算时间差 目前采用开始和发送时间先行计算
                    date1 = time.strptime(startsAt, "%Y-%m-%d %H:%M:%S")
                    date2 = time.strptime(sendtime, "%Y-%m-%d %H:%M:%S")
                    date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
                    date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
                    caltime = str(date2 - date1)
                else:
                    endsAt = alert['endsAt'].split(".")[0] + 'Z'
                    ret_endsAt = utc_to_local(endsAt)
                    ltime_endsAt = time.localtime(ret_endsAt)
                    endsAt = time.strftime("%Y-%m-%d %H:%M:%S", ltime_endsAt)  # 结束时间
                    # 计算时间差 目前采用开始和发送时间先行计算
                    date1 = time.strptime(startsAt, "%Y-%m-%d %H:%M:%S")
                    date2 = time.strptime(endsAt, "%Y-%m-%d %H:%M:%S")
                    date1 = datetime.datetime(date1[0], date1[1], date1[2], date1[3], date1[4], date1[5])
                    date2 = datetime.datetime(date2[0], date2[1], date2[2], date2[3], date2[4], date2[5])
                    caltime = str(date2 - date1)
                if status == "firing":
                    new_status = "😭PROBLEM"
                    tag = "报警"
                    status_color = 'warning'
                else:
                    tag = "恢复"
                    new_status = "😊RECOVERY"
                    status_color = 'info'
                info = """<font color=%s>%s</font> - **%s**
                    ><font color="comment">级别:%s</font>
                    ><font color="comment">发生:%s</font>
                    ><font color="comment">持续:%s</font>
                    ><font color="comment">详情:%s</font>
                    >
                    ><font color="comment">实例:%s</font>
                    ><font color="comment">环境:%s</font>
                    ><font color="comment">机房:%s</font>
                    ><font color="comment">业务:%s</font>
                    ><font color="comment">报警:%s</font>""" % (status_color, tag, alertname, severity, startsAt, caltime, description, ip, env, idc, business,sendtime)
                pushinfo = '''%s-%s
级别:%s
发生:%s
持续:%s
详情:%s

实例:%s
环境:%s
机房:%s
业务:%s
报警:%s''' % (tag,alertname,  severity, startsAt, caltime, description, ip, env, idc, business, sendtime)
                result1 = sendEnterpriseWechat.delay(info)  # 企业微信
                # result2 = sendWechat02(info) #私人微信
                result3 = push_wechat_push_message(pushinfo)
                # time.sleep(5)
                # history alert record存储历史信息
                alertmodels.HistoryAlert.objects.create(alertname=alertname, status=status, severity=severity, env=env,
                                                        idc=idc, business=business, instance=instance, ip=ip, port=port,
                                                        summary=summary, description=description, startsAt=startsAt,
                                                        endsAt=endsAt, sendtime=sendtime, caltime=caltime,
                                                        fingerprint=fingerprint)
                # time_alert
                # 先查询下time alerts 数据库中是否存在此告警信息
                if status == "firing":
                    if alertmodels.TimeAlert.objects.filter(alertname=alertname, ip=ip, business=business):
                        # 存在则更新描述和发送时间,开始时间
                        alertmodels.TimeAlert.objects.filter(alertname=alertname, ip=ip, business=business).update(
                            startsAt=startsAt, sendtime=sendtime, caltime=caltime, description=description)
                    else:
                        # 不存在则存储
                        alertmodels.TimeAlert.objects.create(alertname=alertname, status=status, severity=severity, env=env,
                                                        idc=idc, business=business, instance=instance, ip=ip, port=port,
                                                        summary=summary, description=description, startsAt=startsAt,
                                                        endsAt=endsAt, sendtime=sendtime, caltime=caltime,
                                                        fingerprint=fingerprint)
                elif status == "resolved":
                    alertmodels.TimeAlert.objects.filter(alertname=alertname, ip=ip, business=business).delete()
        except Exception as e:
            print(e)
        finally:
            return HttpResponse(1)

@check_login
def getAlerts(request):
    # print('getAlerts')
    return render(request, 'alarms/history_alert.html')


@check_login
def getTimeLine(request):
    # print('getTimeLine')
    return render(request, 'alarms/timeline.html')


def getTimeLineInfo(request):
    # print('getTimeLineInfo')
    data = alertmodels.TimeAlert.objects.all()
    alarmCount = data.count()
    listAlarmTimeLine = []
    for item in data:
        dictAlarmTimeLine = {}
        dictAlarmTimeLine['id'] = item.id
        dictAlarmTimeLine['alertname'] = item.alertname
        dictAlarmTimeLine['ip'] = item.ip
        dictAlarmTimeLine['env'] = item.env
        dictAlarmTimeLine['idc'] = item.idc
        dictAlarmTimeLine['business'] = item.business
        dictAlarmTimeLine['status'] = item.status
        dictAlarmTimeLine['severity'] = item.severity
        dictAlarmTimeLine['instance'] = item.instance
        dictAlarmTimeLine['port'] = item.port
        dictAlarmTimeLine['summary'] = item.summary
        dictAlarmTimeLine['description'] = item.description
        dictAlarmTimeLine['startsAt'] = item.startsAt
        dictAlarmTimeLine['endsAt'] = item.endsAt
        dictAlarmTimeLine['sendtime'] = item.sendtime
        dictAlarmTimeLine['endsAt'] = item.endsAt
        dictAlarmTimeLine['caltime'] = item.caltime
        dictAlarmTimeLine['fingerprint'] = item.fingerprint
        listAlarmTimeLine.append(dictAlarmTimeLine)
    data = {"code": 0, "msg": "ok", "alarmCount": alarmCount, "data": listAlarmTimeLine}
    return HttpResponse(json.dumps(data))


@check_login
def getTimeAlerts(request):
    # print('getTimeAlerts')
    return render(request, "alarms/time_alert.html")


@check_login
def getServiceRegister(request):
    # print('getServiceRegister')
    return render(request, 'alarms/service_register.html')


# 获取最新注册信息
@check_login
def refreshServiceRegister(request):
    # print('refreshServiceRegister')
    alertmodels.ServicesRegister.objects.all().delete()
    try:
        url = "http://10..27:00/v1/agent/services"
        res_data = requests.get(url)
        content = json.loads(res_data.text)
        services_id = 0
        for info in content:
            services_id = services_id + 1
            service_id = content[info]['ID']
            business = content[info]['Meta']['business']
            env = content[info]['Meta']['env']
            exporter = content[info]['Meta']['exporter']
            hostname = content[info]['Meta']['hostname']
            idc = content[info]['Meta']['idc']
            ip = content[info]['Meta']['ip']
            port = content[info]['Meta']['port']
            alertmodels.ServicesRegister.objects.create(id=services_id, business=business, env=env, idc=idc, ip=ip,
                                                        port=port,
                                                        service_id=service_id,
                                                        exporter=exporter, hostname=hostname)
    except Exception as e:
        print(e)
    # end
    return redirect('/v1/alert/service_register/')


# 查询信息接口
def getTableAlerts(request):
    # print('getTableAlerts')
    search_info = request.GET.get("search_info")
    search_info = str(search_info).strip()
    if search_info != "None":
        querysetData = alertmodels.HistoryAlert.objects.filter(
            Q(id__contains=search_info) | Q(alertname__contains=search_info) | Q(ip__contains=search_info) | Q(
                env__contains=search_info) | Q(idc__contains=search_info) | Q(business__contains=search_info) | Q(
                port__contains=search_info) | Q(severity__contains=search_info) | Q(status__contains=search_info) | Q(
                startsAt__contains=search_info)
            | Q(endsAt__contains=search_info) | Q(sendtime__contains=search_info) | Q(caltime__contains=search_info))
    else:
        querysetData = alertmodels.HistoryAlert.objects.all()
    dataCount = querysetData.count()  # 总条数
    pageIndex = request.GET.get("pageIndex")
    pageSize = request.GET.get("pageSize")
    #获取所需页数据
    pageList=[]
    paginator = Paginator(querysetData,pageSize)
    pageObjects =paginator.page(pageIndex)
    for item in pageObjects:
        dict = {}
        dict['id'] = item.id
        dict['alertname'] = item.alertname
        dict['ip'] = item.ip
        dict['env'] = item.env
        dict['idc'] = item.idc
        dict['business'] = item.business
        dict['status'] = item.status
        dict['severity'] = item.severity
        dict['instance'] = item.instance
        dict['port'] = item.port
        dict['summary'] = item.summary
        dict['description'] = item.description
        dict['startsAt'] = item.startsAt
        dict['endsAt'] = item.endsAt
        dict['sendtime'] = item.sendtime
        dict['endsAt'] = item.endsAt
        dict['caltime'] = item.caltime
        dict['fingerprint'] = item.fingerprint
        pageList.append(dict)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": pageList}
    return HttpResponse(json.dumps(data))


def getTableTimeAlerts(request):
    # print('getTableTimeAlerts')
    querysetData = alertmodels.TimeAlert.objects.all()
    dataCount = querysetData.count()  # 总条数
    pageIndex = request.GET.get("pageIndex")
    pageSize = request.GET.get("pageSize")
    # 获取所需页数据
    pageList = []
    paginator = Paginator(querysetData, pageSize)
    pageObjects = paginator.page(pageIndex)
    for item in pageObjects:
        dict = {}
        dict['id'] = item.id
        dict['alertname'] = item.alertname
        dict['ip'] = item.ip
        dict['env'] = item.env
        dict['idc'] = item.idc
        dict['business'] = item.business
        dict['status'] = item.status
        dict['severity'] = item.severity
        dict['instance'] = item.instance
        dict['port'] = item.port
        dict['summary'] = item.summary
        dict['description'] = item.description
        dict['startsAt'] = item.startsAt
        dict['endsAt'] = item.endsAt
        dict['sendtime'] = item.sendtime
        dict['endsAt'] = item.endsAt
        dict['caltime'] = item.caltime
        dict['fingerprint'] = item.fingerprint
        pageList.append(dict)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": pageList}
    return HttpResponse(json.dumps(data))


def getTableServiceRegister(request):
    # print('getTableServiceRegister')
    search_info = request.GET.get("search_info")
    search_info = str(search_info).strip()
    if search_info != "None":
        querysetData = alertmodels.ServicesRegister.objects.filter(
            Q(id__contains=search_info) | Q(service_id__contains=search_info) | Q(ip__contains=search_info) | Q(
                env__contains=search_info) | Q(idc__contains=search_info) | Q(business__contains=search_info) | Q(
                port__contains=search_info) | Q(hostname__contains=search_info) | Q(exporter__contains=search_info))
    else:
        querysetData = alertmodels.ServicesRegister.objects.all()
    dataCount = querysetData.count()  # 总条数
    pageIndex = request.GET.get("pageIndex")
    pageSize = request.GET.get("pageSize")
    # 获取所需页数据
    pageList = []
    paginator = Paginator(querysetData, pageSize)
    pageObjects = paginator.page(pageIndex)
    for item in pageObjects:
        dict = {}
        dict['id'] = item.id
        dict['service_id'] = item.service_id
        dict['ip'] = item.ip
        dict['env'] = item.env
        dict['idc'] = item.idc
        dict['business'] = item.business
        dict['port'] = item.port
        dict['hostname'] = item.hostname
        dict['exporter'] = item.exporter
        pageList.append(dict)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": pageList}
    return HttpResponse(json.dumps(data))


# 数据分析
# 监控部署分布情况01

@check_login
@completionTime
def MonitorDistribution(request):
    # print("MonitorDistribution")
    servicesList = alertmodels.ServicesRegister.objects.all()
    exporter = list(set(alertmodels.ServicesRegister.objects.values_list('exporter', flat=True)))
    exporter_data = []
    for i in range(0, len(exporter)):
        exporter_data.append(alertmodels.ServicesRegister.objects.filter(exporter=exporter[i]).count())
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(exporter, exporter_data):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    return render(request, 'getDataAnalysis/monitor_distribution.html', {'data': json.dumps(data)})


# 业务监控注册情况02

@check_login
@completionTime
def ServicesRegisterDistribution(request):
    # print("ServicesRegisterDistribution")
    servicesList = alertmodels.ServicesRegister.objects.all()
    business = list(set(alertmodels.ServicesRegister.objects.values_list('business', flat=True)))
    business_data = []
    for i in range(0, len(business)):
        business_data.append(alertmodels.ServicesRegister.objects.filter(business=business[i]).count())
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(business, business_data):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    return render(request, 'getDataAnalysis/services_register_distribution.html', {'data': json.dumps(data)})


# 历史告警类型占比分布03

@check_login
@completionTime
def HistoryAlertDistribution(request):
    # print("HistoryAlertDistribution")
    history_alertList = alertmodels.HistoryAlert.objects.filter(status='firing').all()
    business = list(set(alertmodels.HistoryAlert.objects.values_list('alertname', flat=True)))
    business_data = []
    for i in range(0, len(business)):
        business_data.append(alertmodels.HistoryAlert.objects.filter(alertname=business[i], status='firing').count())
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(business, business_data):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    return render(request, 'getDataAnalysis/history_alert_distribution.html', {'data': json.dumps(data)})


# 业务告警分布情况04

@check_login
@completionTime
def HistoryAlertDistributionOfBusiness(request):
    # print("HistoryAlertDistributionOfBusiness")
    history_alertList = alertmodels.HistoryAlert.objects.filter(status='firing').all()
    business = list(set(alertmodels.HistoryAlert.objects.values_list('business', flat=True)))
    business_data = []
    for i in range(0, len(business)):
        business_data.append(alertmodels.HistoryAlert.objects.filter(business=business[i], status='firing').count())
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(business, business_data):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    return render(request, 'getDataAnalysis/history_alert_distribution_of_business.html', {'data': json.dumps(data)})


# 查询主机告警05

@check_login
@completionTime
def getHostAlertDistribution(request):
    # print('getHostAlertDistribution')
    default_ip = '179.9'
    cmdb_ip = commonmodels.Cmdb.objects.filter(projectenv="prd").all()
    if request.method == 'POST':
        # 'atc_name'：为<select name="atc_name">标签name的值
        data = request.POST.get('atc_name')
        default_ip = data
    history_alertList = alertmodels.HistoryAlert.objects.filter(ip=default_ip, status='firing').all()
    business = list(set(
        alertmodels.HistoryAlert.objects.filter(ip=default_ip, status='firing').all().values_list('alertname',
                                                                                                  flat=True)))
    business_data = []
    for i in range(0, len(business)):
        business_data.append(
            alertmodels.HistoryAlert.objects.filter(alertname=business[i], ip=default_ip, status='firing').count())
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(business, business_data):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    return render(request, 'getDataAnalysis/host_alert_distribution.html', locals())


# 所属业务告警类型占比06

@check_login
@completionTime
def getService_Alarm_type_proportionDistribution(request):
    # print('getService_Alarm_type_proportionDistribution')
    default_business = 'XH'
    types = alertmodels.ServicesRegister.objects.values('business').distinct().order_by('business')
    if request.method == 'POST':
        # 'atc_name'：为<select name="atc_name">标签name的值
        data = request.POST.get('atc_name')
        default_business = data
    history_alertList = alertmodels.HistoryAlert.objects.filter(business=default_business, status='firing').all()
    business = list(set(
        alertmodels.HistoryAlert.objects.filter(business=default_business, status='firing').all().values_list(
            'alertname',
            flat=True)))
    business_data = []
    for i in range(0, len(business)):
        business_data.append(
            alertmodels.HistoryAlert.objects.filter(alertname=business[i], business=default_business,
                                                    status='firing').count())
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(business, business_data):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    return render(request, 'getDataAnalysis/getService_Alarm_type_proportionDistribution.html', locals())


# 业务服务器监控接入情况07

@check_login
@completionTime
def getBusinessServerMonitorDistribution(request):
    # print("getBusinessServerMonitorDistribution")
    servicesList = alertmodels.ServicesRegister.objects.all()
    business = list(
        set(alertmodels.ServicesRegister.objects.filter(exporter="node-exporter").values_list('business', flat=True)))
    business_data = []
    for i in range(0, len(business)):
        business_data.append(
            alertmodels.ServicesRegister.objects.filter(business=business[i], exporter="node-exporter").count())
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(business, business_data):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    return render(request, 'getDataAnalysis/getBusinessServerMonitorDistribution.html', {'data': json.dumps(data)})


# 查询不同告警下各业务告警占比情况08

@check_login
@completionTime
def getDifferentAlarm_Service_proportionDistribution(request):
    # print('getDifferentAlarm_Service_proportionDistribution')
    default_business = '服务器实例异常'
    types = alertmodels.HistoryAlert.objects.values('alertname').distinct().order_by('alertname')
    if request.method == 'POST':
        # 'atc_name'：为<select name="atc_name">标签name的值
        data = request.POST.get('atc_name')
        default_business = data
    history_alertList = alertmodels.HistoryAlert.objects.filter(alertname=default_business, status='firing').all()
    business = list(set(
        alertmodels.HistoryAlert.objects.filter(alertname=default_business, status='firing').all().values_list(
            'business',
            flat=True)))
    business_data = []
    for i in range(0, len(business)):
        business_data.append(
            alertmodels.HistoryAlert.objects.filter(business=business[i], alertname=default_business,
                                                    status='firing').count())
    data = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(business, business_data):
        data.update({k: v, }, )
    # 最后将数据打包成json格式以字典的方式传送到前端
    # return render(request, list_template, {'data': json.dumps(data)},locals())
    return render(request, 'getDataAnalysis/getDifferentAlarm_Service_proportionDistribution.html', locals())


# 获取数据rank 排名情况,用于了解当前告警的业务,告警类型,注册告警情况
# Top_10_Data

@check_login
@completionTime
def getServiceAlarmsTop10Data(request):

    # print('getServiceAlarmsTop10Data')
    # 业务触发告警排名前十
    business = list(set(alertmodels.HistoryAlert.objects.values_list('business', flat=True)))
    business_data = []
    for i in range(0, len(business)):
        business_data.append(alertmodels.HistoryAlert.objects.filter(business=business[i], status='firing').count())
    business_data_dict = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(business, business_data):
        business_data_dict.update({k: v, }, )
    business_data_new = sorted(business_data_dict.items(), key=lambda item: item[1], reverse=True)
    business_data_dict_key = []
    business_data_dict_value = []
    if len(business_data_new) < 10:
        for i in range(0, len(business_data_new)):
            business_data_dict_key.append(business_data_new[i][0])
            business_data_dict_value.append(business_data_new[i][1])
    elif len(business_data_new) >= 10:
        for i in range(0, 10):
            business_data_dict_key.append(business_data_new[i][0])
            business_data_dict_value.append(business_data_new[i][1])
    return render(request, 'getDataRank/Service_Alarms_Top_10_Data.html', locals())


@check_login
@completionTime
def getHostAlarmsTop10Data(request):
    # print('getHostAlarmsTop10Data')
    # 主机告警排名
    host = list(set(alertmodels.HistoryAlert.objects.values_list('ip', flat=True)))
    host_data = []
    for i in range(0, len(host)):
        host_data.append(alertmodels.HistoryAlert.objects.filter(ip=host[i], status='firing').count())
    host_data_dict = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(host, host_data):
        host_data_dict.update({k: v, }, )
    host_data_new = sorted(host_data_dict.items(), key=lambda item: item[1], reverse=True)
    host_data_dict_key = []
    host_data_dict_value = []
    if len(host_data_new) < 10:
        for i in range(0, len(host_data_new)):
            host_data_dict_key.append(host_data_new[i][0])
            host_data_dict_value.append(host_data_new[i][1])
    elif len(host_data_new) >= 10:
        for i in range(0, 10):
            host_data_dict_key.append(host_data_new[i][0])
            host_data_dict_value.append(host_data_new[i][1])
    return render(request, 'getDataRank/Host_Alarms_Top_10_Data.html', locals())


@check_login
@completionTime
def getAlarmTypeTop10Data(request):
    # print('getAlarmTypeTop10Data')
    # 不同类型告警
    alertname = list(set(alertmodels.HistoryAlert.objects.values_list('alertname', flat=True)))
    alertname_data = []
    for i in range(0, len(alertname)):
        alertname_data.append(alertmodels.HistoryAlert.objects.filter(alertname=alertname[i], status='firing').count())
    alertname_data_dict = {}
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for k, v in zip(alertname, alertname_data):
        alertname_data_dict.update({k: v, }, )
    alertname_data_new = sorted(alertname_data_dict.items(), key=lambda item: item[1], reverse=True)
    alertname_data_dict_key = []
    alertname_data_dict_value = []
    if len(alertname_data_new) < 10:
        for i in range(0, len(alertname_data_new)):
            alertname_data_dict_key.append(alertname_data_new[i][0])
            alertname_data_dict_value.append(alertname_data_new[i][1])
    elif len(alertname_data_new) >= 10:
        for i in range(0, 10):
            alertname_data_dict_key.append(alertname_data_new[i][0])
            alertname_data_dict_value.append(alertname_data_new[i][1])
    return render(request, 'getDataRank/Alarm_Type_Top_10_Data.html', locals())


@check_login
@completionTime
def getMonthAlarmsTop10Data(request):
    localdate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 当前时间
    localdate_year = time.strftime("%Y", time.localtime())  # 当前时间
    localdate_year_and_month = time.strftime("%Y-%m", time.localtime())  # 当前时间
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    month_of_alarms = []
    month_of_alarms_dict_key = []
    month_of_alarms_dict_value = []
    month_of_alarms_dict_list = []
    month_of_alarms_dict = {}
    for mon in range(0, len(months)):
        # 当年每月月度告警数排名
        startsAt_year_month = localdate_year + "-" + months[mon]
        month_of_alarms.append(
            alertmodels.HistoryAlert.objects.filter(startsAt__contains=startsAt_year_month, status='firing').count())
    # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
    for key, val in zip(months, month_of_alarms):
        month_of_alarms_dict.update({key: val, }, )
    for keys, value in month_of_alarms_dict.items():
        temp = [keys, value]
        month_of_alarms_dict_list.append(temp)
    for n in range(0, 12):
        month_of_alarms_dict_key.append(month_of_alarms_dict_list[n][0])
        month_of_alarms_dict_value.append(month_of_alarms_dict_list[n][1])
    starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 开始时间
    print("开始时间:", starttime)
    #优化for循环,导致前台展示时间慢
    for i in range(0, len(months)):
        alertname_data_dict_key_i = []
        alertname_data_dict_value_i = []
        # 月度内不同告警数量 1-12月
        # 每个月,最终生成每月的keys values列表
        alertnameList = list(set(alertmodels.HistoryAlert.objects.filter(startsAt__contains=localdate_year + "-" + months[i], ).values_list('alertname', flat=True)))
        print(alertnameList)
        alertnameList_data = []
        alertnameQueryset=alertmodels.HistoryAlert.objects.filter(startsAt__contains=localdate_year + "-" + months[i], ).all()
        for j in range(0, len(alertnameList)):
            alertnameList_data.append(alertnameQueryset.filter(alertname=alertnameList[j], status='firing').count())
        alertname_data_dict = {}
        # keys与values分别为该数据的键数组，值的数组。这里循环为字典添加对应键值
        for k, v in zip(alertnameList, alertnameList_data):
            alertname_data_dict.update({k: v, }, )
        alertname_data_new = sorted(alertname_data_dict.items(), key=lambda item: item[1], reverse=True)
        if len(alertname_data_new) < 10:
            for m in range(0, len(alertname_data_new)):
                alertname_data_dict_key_i.append(alertname_data_new[m][0])
                alertname_data_dict_value_i.append(alertname_data_new[m][1])
        elif len(alertname_data_new) >= 10:
            for m in range(0, 10):
                alertname_data_dict_key_i.append(alertname_data_new[m][0])
                alertname_data_dict_value_i.append(alertname_data_new[m][1])
        if i == 0:
            alertname_data_dict_key_0 = alertname_data_dict_key_i
            alertname_data_dict_value_0 = alertname_data_dict_value_i
        elif i == 1:
            alertname_data_dict_key_1 = alertname_data_dict_key_i
            alertname_data_dict_value_1 = alertname_data_dict_value_i
        elif i == 2:
            alertname_data_dict_key_2 = alertname_data_dict_key_i
            alertname_data_dict_value_2 = alertname_data_dict_value_i
        elif i == 3:
            alertname_data_dict_key_3 = alertname_data_dict_key_i
            alertname_data_dict_value_3 = alertname_data_dict_value_i
        elif i == 4:
            alertname_data_dict_key_4 = alertname_data_dict_key_i
            alertname_data_dict_value_4 = alertname_data_dict_value_i
        elif i == 5:
            alertname_data_dict_key_5 = alertname_data_dict_key_i
            alertname_data_dict_value_5 = alertname_data_dict_value_i
        elif i == 6:
            alertname_data_dict_key_6 = alertname_data_dict_key_i
            alertname_data_dict_value_6 = alertname_data_dict_value_i
        elif i == 7:
            alertname_data_dict_key_7 = alertname_data_dict_key_i
            alertname_data_dict_value_7 = alertname_data_dict_value_i
        elif i == 8:
            alertname_data_dict_key_8 = alertname_data_dict_key_i
            alertname_data_dict_value_8 = alertname_data_dict_value_i
        elif i == 9:
            alertname_data_dict_key_9 = alertname_data_dict_key_i
            alertname_data_dict_value_9 = alertname_data_dict_value_i
        elif i == 10:
            alertname_data_dict_key_10 = alertname_data_dict_key_i
            alertname_data_dict_value_10 = alertname_data_dict_value_i
        elif i == 11:
            alertname_data_dict_key_11 = alertname_data_dict_key_i
            alertname_data_dict_value_11 = alertname_data_dict_value_i
    endtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 结束时间
    print("结束时间", endtime)
    return render(request, 'getDataRank/Month_Alarms_Top_10_Data.html', locals())


# 异常处理方法
def TroubleshootingSuggestions(request):
    pass


