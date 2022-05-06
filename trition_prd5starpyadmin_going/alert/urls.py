from django.conf.urls import url
from django.views.decorators.cache import cache_page
from alert import views

urlpatterns = [
    url(r'^monitor_distribution/', views.MonitorDistribution),
    url(r'^getBusinessServerMonitorDistribution/',views.getBusinessServerMonitorDistribution),
    url(r'^services_register_distribution/', views.ServicesRegisterDistribution),
    url(r'^business_history_alert_distribution/', views.HistoryAlertDistributionOfBusiness),
    url(r'^history_alert_distribution/', views.HistoryAlertDistribution),
    url(r'^host_alert_distribution/', views.getHostAlertDistribution),
    url(r'^getService_Alarm_type_proportionDistribution/', views.getService_Alarm_type_proportionDistribution),
    url(r'^getDifferentAlarm_Service_proportionDistribution/',views.getDifferentAlarm_Service_proportionDistribution),
    url(r'^getServiceAlarmsTop10Data/',views.getServiceAlarmsTop10Data),
    url(r'^getMonthAlarmsTop10Data/', views.getMonthAlarmsTop10Data),
    url(r'^getHostAlarmsTop10Data/', views.getHostAlarmsTop10Data),
    url(r'^getAlarmTypeTop10Data/', views.getAlarmTypeTop10Data),
    url(r'^history_alert/', views.getAlerts),
    url(r'^alarmtimeline/', views.getTimeLine),
    url(r'^getTimeLineInfo/', views.getTimeLineInfo),
    url(r'^host_alert_distribution/', views.getHostAlertDistribution),
    url(r'^webhook/', views.webhook),
    url(r'^time_alert/', views.getTimeAlerts),
    url(r'^service_register/', views.getServiceRegister),
    url(r'^refreshServiceRegister/', views.refreshServiceRegister),
    url(r'^table/alerts/', views.getTableAlerts),
    url(r'^table/time_alerts/', views.getTableTimeAlerts),
    url(r'^table/service_register/', views.getTableServiceRegister),
]
