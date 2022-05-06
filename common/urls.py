from django.conf.urls import url

from common import views

urlpatterns = [
    url(r'^home/', views.home),
    url(r'^cmdb/detectedHost/', views.detectedHost),
    url(r'^detectingsurvival/', views.detectingSurvival),
    url(r'^cmdb/', views.getCmdb),
    url(r'^table/cmdbinfo/', views.getTableCmdb),
    url(r'^refreshcmdb/', views.refreshCmdb),
    url(r'^mysqlreplication/', views.getMysqlReplication),
    url(r'^table/mysqlreplicationinfo/', views.getTableMysqlReplication),
    url(r'^refreshMysqlReplication/', views.refreshMysqlReplication),
    url(r'^todaycmdb/', views.getTodayCmdb),
    url(r'^table/todaycmdbinfo/', views.getTableTodayCmdb),
    url(r'^refreshTodayCmdb/', views.refreshTodayCmdb),
    url(r'^nomonitorcmdb/', views.getNoMonitorCmdb),
    url(r'^table/nomonitorcmdbinfo/', views.getTableNoMonitorCmdb),
    url(r'^refreshNoMonitorCmdb/', views.refreshNoMonitorCmdb),
    url(r'^dtjk/getStatus500Data/', views.getStatus500Data),
    url(r'^dtjk/getStatus404Data/', views.getStatus404Data),
    url(r'^dtjk/Status500Data/', views.Status500Data),
    url(r'^dtjk/Status404Data/', views.Status404Data),
]
