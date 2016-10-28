"""mypro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from myapp import views as myapp_view
urlpatterns = (
    url(r'^$', myapp_view.index, name='index'),
    url(r'^accounts/login/$',myapp_view.login,name='login'),
    url(r'^accounts/logout/$',myapp_view.logout,name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^mysql_query/$', myapp_view.mysql_query,name='mysql_query'),
)
