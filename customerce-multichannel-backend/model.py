import datetime
import os

from django.core.files.storage import default_storage
from django.db import models
from django.utils import timezone

from . import settings


class Shop(models.Model):
    __tablename__ = 'shop'
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=45)
    billing_id = models.CharField(max_length=15)
    script_tag_id = models.CharField(max_length=15)
    app_enabled = models.BooleanField(default=False)
    whatsapp_active = models.BooleanField(default=False)
    facebook_active = models.BooleanField(default=False)
    email_active = models.BooleanField(default=False)
    email = models.EmailField(default=None)
    facebook_page = models.CharField(max_length=90)
    whatsapp_number = models.CharField(max_length=15)
    whatsapp_text = models.CharField(max_length=128)
    panel_color = models.CharField(max_length=6)
    panel_title = models.CharField(max_length=45)
    install_date = models.DateTimeField(auto_now=False)
    free_billing = models.BooleanField()

    class Meta:
        db_table = 'shop'

    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.app_enabled = False
        self.panel_title = 'Contact us'
        self.panel_color = '5ee4ff'
        self.install_date = timezone.now()

    def get_image(self):
        try:
            with open('{}/{}.png'.format(settings.AVATAR_PATH, self.name), "rb") as f:
                return f.read()
        except FileNotFoundError:
            with open('{}/default.png'.format(settings.AVATAR_PATH), "rb") as f:
                return f.read()

    def save_image(self, file):
        dest = '{}/{}.png'.format(settings.AVATAR_PATH, self.name)
        try:
            with default_storage.open(dest, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        except AttributeError:
            os.remove(dest)

    def get_trial_period(self):
        installed = datetime.datetime.strptime(str(self.install_date)[:19], '%Y-%m-%d %H:%M:%S')
        today = datetime.datetime.today()
        period = settings.APP_TRIAL_PERIOD - (today - installed).days

        if period < 0:
            return 0
        if period > settings.APP_TRIAL_PERIOD:
            return settings.APP_TRIAL_PERIOD
        return period


class Notification(models.Model):
    id = models.IntegerField
    background_color = models.CharField(max_length=6)
    font_color = models.CharField(max_length=6)
    text = models.TextField(max_length=6)
    time = models.IntegerField()
    url = models.CharField(max_length=2083)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column="shop_id")

    class Meta:
        db_table = 'notification'

    def serialize(self):
        return {
            'id': self.id,
            'background_color': self.background_color,
            'font_color': self.font_color,
            'text': self.text,
            'time': self.time,
            'url': self.url
        }


class Faq(models.Model):
    id = models.IntegerField
    question = models.TextField()
    answer = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column="shop_id")

    class Meta:
        db_table = 'faq'

    def serialize(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer
        }
