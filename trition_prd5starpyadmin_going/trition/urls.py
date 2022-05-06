"""trition URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.urls import re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.views import serve


import user.views


def return_static(request, path, insecure=True, **kwargs):
    return serve(request, path, insecure, **kwargs)


urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^update_password/', user.views.updatePassword),
                  re_path(r'^static/(?P<path>.*)$', return_static, name='static'),
                  # 分发到其他app url
                  url(r'^v1/alert/', include('alert.urls')),  # app alert
                  url(r'^v1/user/', include('user.urls')),  # app user
                  url(r'^v1/', include('common.urls')),  # app common
                  url(r'^', include('user.urls')),  # app user
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# 404 页面找不到
handler404 = user.views.page_not_find
# 500 服务器出错
handler500 = user.views.page_error
# 资源不可用
handler403 = user.views.resources_not_available
