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
from django.urls import path

from .api import api_views, notification_api, faq_api, email_api, script_tag_api
import redirect_api
from .views import render_base_page, render_faq_page, render_notification_page

APP_URL = 'app/'
API_URL = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('redirect', redirect_api.redirect),
    path('install', redirect_api.install),
    path('install/confirm', redirect_api.confirm),
    path(APP_URL, render_base_page),
    path(APP_URL + 'faq', render_faq_page),
    path(APP_URL + 'notification', render_notification_page),
    path(API_URL + 'shop/<str:shopname>', api_views.chat_info),
    path(API_URL + 'shop/image/<str:shopname>', api_views.get_avatar_image),
    path(API_URL + 'notification/<int:shop_id>', notification_api.get_all_from_shop),
    path(API_URL + 'faq/<int:shop_id>', faq_api.get_all_from_shop),
    path(API_URL + 'sendemail', email_api.send),
    path(API_URL + 'scriptag', script_tag_api.script),
]
