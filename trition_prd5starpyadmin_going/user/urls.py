from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^getlogin/', views.getlogin),
    url(r'^logout/', views.logout),
    url(r'^getupdatepasswd/', views.getUpdatePassword),
]
