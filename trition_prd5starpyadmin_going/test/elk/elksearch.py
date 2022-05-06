from elasticsearch import Elasticsearch
from elasticsearch_dsl.search import Search, Q, A
import os
import time
def search_500():
    client = Elasticsearch([{'host': '172.20.0.118', 'port': 9200}], http_auth=('elastic', 'Spring01'), timeout=3600)
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "status": "500"
                        }
                    }
                ],
                "filter": {
                    "range": {
                        '@timestamp': {
                            "gt": "now-1m",
                            "lt": "now"
                        }
                    }
                }
            }
        }
    }
    ret=client.count(body=body)
    return ret

def search_404():
    client = Elasticsearch([{'host': '172.20.0.118', 'port': 9200}], http_auth=('elastic', 'Spring01'), timeout=3600)
    body = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "status": "404"
                        }
                    }
                ],
                "filter": {
                    "range": {
                        '@timestamp': {
                            "gt": "now-1m",
                            "lt": "now"
                        }
                    }
                }
            }
        }
    }
    ret=client.count(body=body)
    return ret

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trition.settings")  # 文件内容在自己项目的wsgi.py文件中第14行
    import django
    django.setup()
    from common import models
    while True:
        searchtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # 发送时间
        search_time_stamp=time.time() # 发送时间戳
        print(searchtime)
        ret500=search_500()
        ret404=search_404()
        status_500 =ret500["count"]
        status_404 =ret404["count"]
        print(ret404)
        print(ret500)
        print(status_500)
        print(status_404)
        models.elkNginxStatus500.objects.create(status_500=status_500,search_time=searchtime,search_time_stamp=search_time_stamp)
        models.elkNginxStatus404.objects.create(status_404=status_404,search_time=searchtime,search_time_stamp=search_time_stamp)
        time.sleep(60)

