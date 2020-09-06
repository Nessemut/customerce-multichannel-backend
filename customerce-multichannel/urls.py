"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .api_views import *
from .redirect_api import *
from .views import *

APP_URL = 'app/'
API_URL = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redirect', redirect),
    path('install', install),
    path('install/confirm', confirm),
    path('', render_channels_page),
    path(APP_URL, render_shop_page),
    path(APP_URL + 'shop', render_shop_page),
    path(APP_URL + 'channels', render_channels_page),
    path(APP_URL + 'faq', render_faq_page),
    path(APP_URL + 'notification', render_notification_page),
    path(APP_URL + 'notification/<int:id>', notification_create),
    path(API_URL + 'shop/<str:shopname>', ShopApi.chat_info),
    path(API_URL + 'shop/image/<str:shopname>', ShopApi.get_avatar_image),
    path(API_URL + 'notification/<int:shop_id>', NotificationApi.get_all),
    path(API_URL + 'faq/<int:shop_id>', FaqApi.get_all),
    path(API_URL + 'sendemail', EmailApi.send),
    path(API_URL + 'scriptag', ScriptTagApi.script),
]
