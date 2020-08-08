from django.shortcuts import render
from django.contrib.auth import authenticate

shop = authenticate(username='john', password='secret')


def render_base_page(request):
    return render(request, 'base.html')


def render_faq_page(request):
    return render(request, 'faq.html')


def render_notification_page(request):
    return render(request, 'notification.html')
