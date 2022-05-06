import json
import os
import time
import django
import paramiko
import requests
import random
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from user.views import check_login

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trition.settings")
django.setup()

from alert.models import *
from common import models


# Create your views here.
#dtjk from elk 404 500
def getStatus500Data(request):
    data_all = sorted(list(set(models.elkNginxStatus500.objects.values_list().order_by('search_time'))))
    data_all= data_all[-60:] #取60个点,即1h
    search_time=[]
    status500_data=[]
    for num in range(0,len(data_all)):
        search_time.append(data_all[num][2])
        status500_data.append(data_all[num][1])
    # search_time = sorted(list(set(models.elkNginxStatus500.objects.values_list('search_time', flat=True))))
    # search_time = search_time[-60:]
    # status500_data = []
    # for i in range(0, len(search_time)):
    #     status500 = models.elkNginxStatus500.objects.get(search_time=search_time[i]).status_500
    #     status500_data.append(status500)
    data = {"datas": {"search_time": search_time, "status500_data": status500_data}}
    return HttpResponse(json.dumps(data))

def Status404Data(request):
    return render(request,'dtjk/dtjkstatus404.html')

def getStatus404Data(request):
    search_time = sorted(list(set(models.elkNginxStatus404.objects.values_list('search_time', flat=True))))
    search_time = search_time[-60:]
    status404_data = []
    for i in range(0, len(search_time)):
        status404 = models.elkNginxStatus404.objects.get(search_time=search_time[i]).status_404
        status404_data.append(status404)
    data = {"datas": {"search_time": search_time, "status404_data": status404_data}}
    return HttpResponse(json.dumps(data))

def Status500Data(request):
    return render(request,'dtjk/dtjkstatus500.html')
# 监控主页,展示当前监控服务器与服务组件,和告警信息相关数据
@check_login
def home(request):
    # print('home')
    # from consul
    node_exporter = ServicesRegister.objects.filter(exporter='node-exporter').count()
    mysqld_exporter = ServicesRegister.objects.filter(exporter='mysqld-exporter').count()
    redis_exporter = ServicesRegister.objects.filter(exporter='redis-exporter').count()
    zookeeper_exporter = ServicesRegister.objects.filter(exporter='zookeeper-exporter').count()
    oracledb_exporter = ServicesRegister.objects.filter(exporter='oracledb-exporter').count()
    rabbitmq_exporter = ServicesRegister.objects.filter(exporter='rabbitmq-exporter').count()
    mongodb_exporter = ServicesRegister.objects.filter(exporter='mongodb-exporter').count()
    elasticsearch_exporter = ServicesRegister.objects.filter(exporter='elasticsearch-exporter').count()
    kafka_exporter = ServicesRegister.objects.filter(exporter='kafka-exporter').count()
    blackbox_exporter = ServicesRegister.objects.filter(exporter='blackbox-exporter').count()
    windows_exporter = ServicesRegister.objects.filter(exporter='windows-exporter').count()
    # from histtory alert
    histtory_alerts = HistoryAlert.objects.filter(status='firing').count()
    time_alerts = TimeAlert.objects.filter(status='firing').count()
    # email = request.session.get('email', False)  # 获取登录用户email
    return render(request, 'base/home.html', locals())


# 执行command 相关函数start
# 机器探活
@check_login
def detectingSurvival(request):
    # print('DetectingSurvival')
    return render(request, 'commond/DetectingSurvival.html')


# 机器探活 执行ping探测
@csrf_exempt
def detectedHost(request):
    # print(detectedHost)
    local_host = "10.22"  # 使用本机进行ping探测
    # 'detected_host'：为<input name="detected_host">标签name的值
    detected_host = request.POST.get('detected_host').strip()
    ping_commond = "ping -c4" + " " + detected_host
    # start 远程执行
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        file_abspath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'PathInformation')
        file = os.path.join(file_abspath, 'file_abspath')
        key = paramiko.RSAKey.from_private_key_file(file)
        client.connect(hostname=local_host, username='root', pkey=key)
        stdin, stdout, stderr = client.exec_command(ping_commond)
        # 获取命令结果
        result = stdout.read()
        # 打印输出
        rescommondinfo = result.decode()
    except Exception as e:
        print("%s:%s" % (e.__class__, e))
    finally:
        # 关闭
        client.close()
    # end 远程执行
    start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 发送时间
    res_data = {
        "host": detected_host,
        "rescommondinfo": rescommondinfo,
        "starttime": start_time,
    }
    data = {"code": 0, "msg": "ok", "data": res_data}
    return HttpResponse(json.dumps(data))



# 执行command 相关函数 end

# 获取cmdb机器信息
@check_login
def getCmdb(request):
    # print('getCmdb')
    return render(request, 'cmdb/cmdb.html')

# 数据表
def getTableCmdb(request):
    # print('getTableCmdb')
    search_info = request.GET.get("search_info")
    search_info = str(search_info).strip()
    if search_info != "None":
        querysetData = models.Cmdb.objects.filter(Q(serverip__contains=search_info) | Q(projectname__contains=search_info) | Q(
            projectadmin__contains=search_info) | Q(cmdb_id__contains=search_info) | Q(
            hostname__contains=search_info) | Q(
            cpuinfo__contains=search_info) | Q(diskinfo__contains=search_info) | Q(
            meminfo__contains=search_info) | Q(datacenter__contains=search_info) | Q(
            projectenv__contains=search_info) | Q(createtime__contains=search_info) | Q(
            status__contains=search_info) | Q(ostype__contains=search_info))
    else:
        querysetData = models.Cmdb.objects.all()
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
        dict['cmdb_id'] = item.cmdb_id
        dict['hostname'] = item.hostname
        dict['serverip'] = item.serverip
        dict['cpuinfo'] = item.cpuinfo
        dict['diskinfo'] = item.diskinfo
        dict['meminfo'] = item.meminfo
        dict['datacenter'] = item.datacenter
        dict['ostype'] = item.ostype
        dict['projectname'] = item.projectname
        dict['projectenv'] = item.projectenv
        dict['projectadmin'] = item.projectadmin
        dict['createtime'] = item.createtime
        dict['status'] = item.status
        pageList.append(dict)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": pageList}
    return HttpResponse(json.dumps(data))

# 刷新
@check_login
def refreshCmdb(request):
    # print('refreshCmdb')
    # cmdb 变量
    page_num = 2
    cmdb_info_id = 0
    product_info_id = 0
    try:
        token_url = "https:/star.com/api/token/"
        query_args = {
            "username": 'wwwww',
            "password": 'qwwwqw'
        }
        resp = requests.post(url=token_url, data=query_args)
        # print(json.loads(resp.text))
        # print(json.loads(resp.text)["data"]["token"])
        get_token = json.loads(resp.text)["data"]["token"]
        # 将获取的token，拼成headers
        new_headers = {"Authorization": "JWT" + " " + get_token}
        # 获取产品信息
        # start
        product_url = "https://star.com/cmdb/product/?page_size=200"
        product_res = requests.get(product_url, headers=new_headers)
        product_res_data = json.loads(product_res.text)
        new_product_res_data = product_res_data['data']['content']
        models.Product.objects.all().delete()
        models.Cmdb.objects.all().delete()
        for item in new_product_res_data:
            # print(item)
            id = item['id']
            projectname = item['product_name']
            createtime = item['created_at'].replace("T", " ")
            modifytime = item['updated_at'].replace("T", " ")
            status = item['life_cycle_display']
            models.Product.objects.create(id=id, projectname=projectname, createtime=createtime, modifytime=modifytime,
                                          status=status)
        # end
        projectname = models.Product.objects.filter(id=1)
        # start get cmdb info
        for i in range(1, page_num + 1):
            base_url = "https://star.com/cmdb/server/?page_size=1000&page="
            url = ''.join([base_url, str(i)])
            # 个人信息请勿擅自使用,将追究法律责任
            res = requests.get(url, headers=new_headers)
            # print(res)
            res_data = json.loads(res.text)
            new_res_data = res_data['data']['content']
            for info in new_res_data:
                cmdb_info_id = cmdb_info_id + 1
                cmdb_id = info['id']
                hostname = info['virtual_name']
                serverip = info['ipaddress']
                cpuinfo = info['cpu']
                diskinfo = info['disk']
                meminfo = info['mem']
                datacenter = info['dc_display']
                ostype = info['os_display']
                projectname = info['product']
                if projectname:
                    projectname = models.Product.objects.filter(id=info['product']).first()
                else:
                    pass
                # projectname = info['remarks']
                projectenv = info['env']
                if projectenv:
                    projectenv = projectenv.upper()
                else:
                    pass
                projectadmin = info['operator']
                createtime = info['created_at'].replace("T", " ")
                modifytime = info['updated_at'].replace("T", " ")
                status = info['state_display']
                models.Cmdb.objects.create(id=cmdb_info_id, cmdb_id=cmdb_id, hostname=hostname, serverip=serverip,
                                           cpuinfo=cpuinfo,
                                           diskinfo=diskinfo, meminfo=meminfo, datacenter=datacenter, ostype=ostype,
                                           projectname=projectname, projectenv=projectenv, projectadmin=projectadmin,
                                           createtime=createtime, modifytime=modifytime, status=status)
            # end
    except Exception as e:
        print(e)
    return redirect('/v1/cmdb/')


# cmdb与consul注册机器进行差分,获取未监控主机
@check_login
def getNoMonitorCmdb(request):
    # print('getNoMonitorCmdb')
    return render(request, 'cmdb/no_monitor_cmdb.html')

def getTableNoMonitorCmdb(request):
    search_info = request.GET.get("search_info")
    search_info = str(search_info).strip()
    # print(search_info)
    if search_info != "None":
        querysetData = models.NoMonitorCmdb.objects.filter(
            Q(serverip__contains=search_info) | Q(projectname__contains=search_info) | Q(
                projectadmin__contains=search_info) | Q(cmdb_id__contains=search_info) | Q(
                hostname__contains=search_info) | Q(
                cpuinfo__contains=search_info) | Q(diskinfo__contains=search_info) | Q(
                meminfo__contains=search_info) | Q(datacenter__contains=search_info) | Q(
                projectenv__contains=search_info) | Q(createtime__contains=search_info) | Q(
                status__contains=search_info) | Q(ostype__contains=search_info))
    else:
        querysetData = models.NoMonitorCmdb.objects.all()
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
        dict['cmdb_id'] = item.cmdb_id
        dict['hostname'] = item.hostname
        dict['serverip'] = item.serverip
        dict['cpuinfo'] = item.cpuinfo
        dict['diskinfo'] = item.diskinfo
        dict['meminfo'] = item.meminfo
        dict['datacenter'] = item.datacenter
        dict['ostype'] = item.ostype
        dict['projectname'] = item.projectname
        dict['projectenv'] = item.projectenv
        dict['projectadmin'] = item.projectadmin
        dict['createtime'] = item.createtime
        dict['status'] = item.status
        pageList.append(dict)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": pageList}
    return HttpResponse(json.dumps(data))

# 刷新
@check_login
def refreshNoMonitorCmdb(request):
    # print('refreshNoMonitorCmdb')
    new_machine_id = 0
    models.NoMonitorCmdb.objects.all().delete()
    consul_node_ip = []
    cmdb_machine_ip = []
    consul_node_ip = ServicesRegister.objects.filter(
        Q(exporter="node-exporter") | Q(exporter="windows-exporter")).values_list('ip')
    cmdb_machine_ip = models.Cmdb.objects.filter(projectenv="PRD", status="运行中").values_list('serverip')
    new_machine_ip = list(set(cmdb_machine_ip) - set(consul_node_ip))
    for i in range(0, len(new_machine_ip)):
        ip = new_machine_ip[i][0]
        L = list(models.Cmdb.objects.filter(serverip=ip).values_list())
        for j in range(0, len(L)):
            new_machine_id = new_machine_id + 1
            cmdb_id = L[j][1]
            hostname = L[j][2]
            serverip = L[j][3]
            cpuinfo = L[j][4]
            diskinfo = L[j][5]
            meminfo = L[j][6]
            projectname = L[j][7]
            ostype = L[j][8]
            datacenter = L[j][9]
            projectenv = L[j][10]
            projectadmin = L[j][11]
            createtime = L[j][12]
            modifytime = L[j][13]
            status = L[j][14]
            models.NoMonitorCmdb.objects.create(id=new_machine_id, cmdb_id=cmdb_id, hostname=hostname,
                                                serverip=serverip,
                                                cpuinfo=cpuinfo,
                                                diskinfo=diskinfo, meminfo=meminfo, datacenter=datacenter,
                                                ostype=ostype,
                                                projectname=projectname, projectenv=projectenv,
                                                projectadmin=projectadmin,
                                                createtime=createtime, modifytime=modifytime, status=status)
    return redirect('/v1/nomonitorcmdb/')


# 获取今日新增机器
@check_login
def getTodayCmdb(request):
    # print('getTodayCmdb')
    return render(request, 'cmdb/today_cmdb.html')

def getTableTodayCmdb(request):
    # time_today = time.strftime("%Y-%m-%d", time.localtime())
    search_info = request.GET.get("search_info")
    search_info = str(search_info).strip()
    # print(search_info)
    if search_info != "None":
        querysetData = models.TodayCmdb.objects.filter(
            Q(serverip__contains=search_info) | Q(projectname__contains=search_info) | Q(
                projectadmin__contains=search_info) | Q(cmdb_id__contains=search_info) | Q(
                hostname__contains=search_info) | Q(
                cpuinfo__contains=search_info) | Q(diskinfo__contains=search_info) | Q(
                meminfo__contains=search_info) | Q(datacenter__contains=search_info) | Q(
                projectenv__contains=search_info) | Q(createtime__contains=search_info) | Q(
                status__contains=search_info) | Q(ostype__contains=search_info))
    else:
        # data = models.Cmdb.objects.filter(createtime__contains=time_today)
        querysetData = models.TodayCmdb.objects.all()
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
        dict['cmdb_id'] = item.cmdb_id
        dict['hostname'] = item.hostname
        dict['serverip'] = item.serverip
        dict['cpuinfo'] = item.cpuinfo
        dict['diskinfo'] = item.diskinfo
        dict['meminfo'] = item.meminfo
        dict['datacenter'] = item.datacenter
        dict['ostype'] = item.ostype
        dict['projectname'] = item.projectname
        dict['projectenv'] = item.projectenv
        dict['projectadmin'] = item.projectadmin
        dict['createtime'] = item.createtime
        dict['status'] = item.status
        pageList.append(dict)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": pageList}
    return HttpResponse(json.dumps(data))


# 刷新
@check_login
def refreshTodayCmdb(request):
    # print('refreshTodayCmdb')
    time_today = time.strftime("%Y-%m-%d", time.localtime())
    # cmdb 变量
    page_num = 2
    cmdb_info_id = 0
    product_info_id = 0
    try:
        token_url = "star.com/api/token/"
        query_args = {
            "username": 'qweqwe',
            "password": 'ewqcac'
        }
        resp = requests.post(url=token_url, data=query_args)
        # print(json.loads(resp.text))
        # print(json.loads(resp.text)["data"]["token"])
        get_token = json.loads(resp.text)["data"]["token"]
        # 将获取的token，拼成headers
        new_headers = {"Authorization": "JWT" + " " + get_token}
        # 获取产品信息
        # start
        product_url = "star.com/cmdb/product/?page_size=200"
        product_res = requests.get(product_url, headers=new_headers)
        product_res_data = json.loads(product_res.text)
        new_product_res_data = product_res_data['data']['content']
        # print(new_product_res_data)
        models.Product.objects.all().delete()
        models.TodayCmdb.objects.all().delete()
        for item in new_product_res_data:
            # print(item)
            id = item['id']
            projectname = item['product_name']
            createtime = item['created_at'].replace("T", " ")
            modifytime = item['updated_at'].replace("T", " ")
            status = item['life_cycle_display']
            models.Product.objects.create(id=id, projectname=projectname, createtime=createtime, modifytime=modifytime,
                                          status=status)
        # end
        projectname = models.Product.objects.filter(id=1)
        # print(projectname)
        # start get cmdb info
        for i in range(1, page_num + 1):
            base_url = "star.com/cmdb/server/?page_size=1000&page="
            url = ''.join([base_url, str(i)])
            # 个人信息请勿擅自使用,将追究法律责任
            res = requests.get(url, headers=new_headers)
            # print(res)
            res_data = json.loads(res.text)
            new_res_data = res_data['data']['content']
            # print(new_res_data)
            for info in new_res_data:
                cmdb_id = info['id']
                hostname = info['virtual_name']
                serverip = info['ipaddress']
                cpuinfo = info['cpu']
                diskinfo = info['disk']
                meminfo = info['mem']
                datacenter = info['dc_display']
                ostype = info['os_display']
                projectname = info['product']
                if projectname:
                    projectname = models.Product.objects.filter(id=info['product']).first()
                else:
                    pass
                # projectname = info['remarks']
                projectenv = info['env']
                if projectenv:
                    projectenv = projectenv.upper()
                else:
                    pass
                projectadmin = info['operator']
                createtime = info['created_at'].replace("T", " ")
                modifytime = info['updated_at'].replace("T", " ")
                status = info['state_display']
                if createtime.split(" ")[0] == time_today:
                    cmdb_info_id = cmdb_info_id + 1
                    models.TodayCmdb.objects.create(id=cmdb_info_id, cmdb_id=cmdb_id, hostname=hostname, serverip=serverip,
                                           cpuinfo=cpuinfo,
                                           diskinfo=diskinfo, meminfo=meminfo, datacenter=datacenter, ostype=ostype,
                                           projectname=projectname, projectenv=projectenv, projectadmin=projectadmin,
                                           createtime=createtime, modifytime=modifytime, status=status)
                else:
                    pass
            # end
    except Exception as e:
        print(e)
    return redirect('/v1/todaycmdb/')


# 获取mysql数据库主从关系
@check_login
def getMysqlReplication(request):
    # print('getMysqlReplication')
    return render(request, 'mysql/mysql_replication.html')


def getTableMysqlReplication(request):
    # print('getTableMysqlReplication')
    search_info = request.GET.get("search_info")
    search_info = str(search_info).strip()
    # print(search_info)
    if search_info != "None":
        querysetData = models.MysqlReplication.objects.filter(
            Q(projectname__contains=search_info) | Q(rp__contains=search_info) | Q(master_ip__contains=search_info) | Q(
                slave_ip__contains=search_info) | Q(rp_status__contains=search_info))
    else:
        querysetData = models.MysqlReplication.objects.all()
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
        dict['projectname'] = item.projectname
        dict['rp'] = item.rp
        dict['master_ip'] = item.master_ip
        dict['slave_ip'] = item.slave_ip
        dict['rp_status'] = item.rp_status
        pageList.append(dict)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": pageList}
    return HttpResponse(json.dumps(data))


# 刷新
@check_login
def refreshMysqlReplication(request):
    models.MysqlReplication.objects.all().delete()
    mysqlreplication_id = 0
    res_ip = list(set(ServicesRegister.objects.filter(exporter='mysqld-exporter').values_list('ip', flat=True)))
    print(res_ip)
    # try:
    for i in range(0, len(res_ip)):
            # start 远程执行
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                file_abspath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                            'PathInformation')
                file = os.path.join(file_abspath, 'file_abspath')
                key = paramiko.RSAKey.from_private_key_file(file)
                client.connect(hostname="10.22", username='root', pkey=key)
                stdin, stdout, stderr = client.exec_command("sh /opt/autoCommond/check_mysql_role.sh " + res_ip[i])
                # 获取命令结果
                result = stdout.read()
                # 打印输出
                rescommondinfo = result.decode()
                # 获取命令结果
                ret = rescommondinfo.split(':')
                if ret[0].strip() == '1':
                    projectname = ServicesRegister.objects.filter(ip=res_ip[i]).values('business', ).first()['business']
                    mysqlreplication_id = mysqlreplication_id + 1
                    models.MysqlReplication.objects.create(id=mysqlreplication_id, master_ip=res_ip[i],
                                                           projectname=projectname, slave_ip='无',
                                                           rp_status='无', rp='单实例')
                elif ret[0].strip() == '2':
                    slave_ips = ret[2].strip().split('/n')[0].split(',')
                    slaves = []
                    str_slaves = ''
                    for j in range(0, len(slave_ips)):
                        if slave_ips[j] in res_ip:
                            # print('slave从数据库已存在注册服务中')
                            slaves.append(slave_ips[j])
                            str_slaves = "(" + slave_ips[j] + ")" + str_slaves
                        else:
                            # print('slave从数据库不存在注册服务中')
                            slaves.append(slave_ips[j] + '✘')
                            str_slaves = "(" + slave_ips[j] + "✘" + ")" + str_slaves
                    projectname = ServicesRegister.objects.filter(ip=res_ip[i]).values('business', ).first()['business']
                    mysqlreplication_id = mysqlreplication_id + 1
                    models.MysqlReplication.objects.create(id=mysqlreplication_id, master_ip=res_ip[i],
                                                           projectname=projectname,
                                                           slave_ip=str_slaves,
                                                           rp_status='ON', rp='主从复制')
                else:
                    master_ip = ret[2].strip().split('/n')[0]
                    if master_ip in res_ip:
                        ret='master主数据库已存在注册服务中'
                    else:
                        ret='master主数据库不存在注册服务中'
                        projectname = ServicesRegister.objects.filter(ip=res_ip[i]).values('business', ).first()[
                            'business']
                        mysqlreplication_id = mysqlreplication_id + 1
                        models.MysqlReplication.objects.create(id=mysqlreplication_id, master_ip=master_ip + '✘',
                                                               projectname=projectname,
                                                               slave_ip=res_ip[i], rp_status='ON', rp='主从复制')
            except Exception as e:
                print("%s:%s" % (e.__class__, e))
            finally:
                # 关闭
                client.close()
    return redirect('/v1/mysqlreplication/')







