from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import *
from . import settings
from .forms import *

#shop = authenticate(username='john', password='secret')
shop = Shop.objects.get(name="customerce-apptest")

def render_shop_page(request):
    return render(request, 'shop.html', {"shop": shop})


def render_channels_page(request):
    return render(request, 'channels.html')


def render_faq_page(request):
    return render(request, 'faq.html', {"faqs": shop.faq_set.all()})


def render_notification_page(request):
    return render(request, 'notification.html', {"notifications": shop.notification_set.all()})


def notification_create(request, id):
    instance = Notification.objects.get(id=id)
    form = NotificationForm(request.POST or None, instance=instance)
    if form.is_valid():
          form.save()
          return render_notification_page(request)
    # TODO: add an error message
    return render_notification_page(request)
