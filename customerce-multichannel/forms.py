from django import forms

from .models import *


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            'app_enabled',
            'panel_title'
        ]


class ChannelsForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = [
            'email_active',
            'facebook_active',
            'whatsapp_active',
            'email',
            'facebook_page',
            'whatsapp_number'
        ]


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['text']


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['question', 'answer']
