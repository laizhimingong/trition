from django.conf.urls import url
from django.views.decorators.cache import cache_page
from alert import views

urlpatterns = [
    url(r'^monitor_distribution/', cache_page(60*15)(views.MonitorDistribution)),
    url(r'^getBusinessServerMonitorDistribution/', cache_page(60*15)(views.getBusinessServerMonitorDistribution)),
    url(r'^services_register_distribution/', cache_page(60*15)(views.ServicesRegisterDistribution)),
    url(r'^business_history_alert_distribution/', cache_page(60*15)(views.HistoryAlertDistributionOfBusiness)),
    url(r'^history_alert_distribution/', cache_page(60*15)(views.HistoryAlertDistribution)),
    url(r'^host_alert_distribution/', cache_page(60*15)(views.getHostAlertDistribution)),
    url(r'^getService_Alarm_type_proportionDistribution/', cache_page(60*15)(views.getService_Alarm_type_proportionDistribution)),
    url(r'^getDifferentAlarm_Service_proportionDistribution/', cache_page(60*15)(views.getDifferentAlarm_Service_proportionDistribution)),
    url(r'^getServiceAlarmsTop10Data/', cache_page(60*15)(views.getServiceAlarmsTop10Data)),
    url(r'^getMonthAlarmsTop10Data/', cache_page(60*15)(views.getMonthAlarmsTop10Data)),
    url(r'^getHostAlarmsTop10Data/', cache_page(60*15)(views.getHostAlarmsTop10Data)),
    url(r'^getAlarmTypeTop10Data/', cache_page(60*15)(views.getAlarmTypeTop10Data)),
    url(r'^history_alert/', cache_page(60*15)(views.getAlerts)),
    url(r'^alarmtimeline/', views.getTimeLine),
    url(r'^getTimeLineInfo/', views.getTimeLineInfo),
    url(r'^host_alert_distribution/', cache_page(60*15)(views.getHostAlertDistribution)),
    url(r'^webhook/', views.webhook),
    url(r'^time_alert/', views.getTimeAlerts),
    url(r'^service_register/', views.getServiceRegister),
    url(r'^refreshServiceRegister/', views.refreshServiceRegister),
    url(r'^table/alerts/', cache_page(60*15)(views.getTableAlerts)),
    url(r'^table/time_alerts/', views.getTableTimeAlerts),
    url(r'^table/service_register/', views.getTableServiceRegister),
]
