from django import forms

from .models import *


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['email', 'whatsapp_text']


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['text']


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ['question', 'answer']
