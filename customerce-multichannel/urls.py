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
from . import redirect_api
from . import views

APP_URL = 'app/'
API_URL = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redirect', redirect_api.redirect),
    path('install', install),
    path('install/confirm', confirm),
    path('', views.render_channels_page),
    path(APP_URL, views.render_shop_page),
    path(APP_URL + 'shop', views.render_shop_page),
    path(APP_URL + 'channels', views.render_channels_page),
    path(APP_URL + 'faq', views.render_faq_page),
    path(APP_URL + 'notification', views.render_notification_page),
    path(APP_URL + 'notification/create/', views.notification_create),
    path(APP_URL + 'notification/update/<int:id>', views.notification_update),
    path(APP_URL + 'notification/delete/<int:id>', views.notification_delete),
    path(APP_URL + 'faq/create/', views.faq_create),
    path(APP_URL + 'faq/update/<int:id>', views.faq_update),
    path(APP_URL + 'faq/delete/<int:id>', views.faq_delete),
    path(API_URL + 'shop/<str:shopname>', ShopApi.chat_info),
    path(API_URL + 'shop/image/<str:shopname>', ShopApi.get_avatar_image),
    path(API_URL + 'notification/<int:shop_id>', NotificationApi.get_all),
    path(API_URL + 'faq/<int:shop_id>', FaqApi.get_all),
    path(API_URL + 'sendemail', EmailApi.send),
    path(API_URL + 'scriptag', ScriptTagApi.script),
]
