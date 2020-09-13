import datetime
import os

from django.core.files.storage import default_storage
from django.db import models
from django.utils import timezone

from . import settings


class Shop(models.Model):
    name = models.CharField(max_length=30, db_column='name', unique=True)
    token = models.CharField(max_length=45, null=True)
    billing_id = models.IntegerField(null=True)
    script_tag_id = models.IntegerField(null=True)
    billing_accepted = models.BooleanField(null=False, default=False)
    app_enabled = models.BooleanField(default=False, null=True)
    whatsapp_active = models.BooleanField(default=False, null=False)
    facebook_active = models.BooleanField(default=False, null=False)
    email_active = models.BooleanField(default=False, null=False)
    email = models.EmailField(default=None, null=True)
    facebook_page = models.CharField(max_length=90, null=True)
    whatsapp_number = models.CharField(max_length=15, null=True)
    whatsapp_text = models.CharField(max_length=128, null=True)
    panel_color = models.CharField(max_length=6, null=True)
    panel_title = models.CharField(max_length=45, null=True)
    install_date = models.DateTimeField(auto_now=False, null=True)
    free_billing = models.BooleanField(default=False, null=True)

    class Meta:
        db_table = 'shop'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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

    def get_avatar_path(self):
        custom_image = settings.AVATAR_PATH + '/' + self.name + '.png'
        if os.path.isfile(settings.BASE_DIR + custom_image):
            return custom_image
        return settings.AVATAR_PATH + '/default.png'

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

    def serialize(self):
        res = {
            'id': self.id,
            'name': self.name,
            'facebook_active': self.facebook_active,
            'whatsapp_active': self.whatsapp_active,
            'email_active': self.email_active,
            'panel_color': self.panel_color,
            'panel_title': self.panel_title
        }
        if self.facebook_active:
            res['facebook_page'] = self.facebook_page
        if self.email_active:
            res['email'] = self.email
        if self.whatsapp_active:
            res['whatsapp_number'] = self.whatsapp_number
            res['whatsapp_text'] = self.whatsapp_text

        return res


class Notification(models.Model):
    id = models.IntegerField
    background_color = models.CharField(max_length=6)
    font_color = models.CharField(max_length=6)
    text = models.TextField(max_length=128)
    time = models.IntegerField(default=60)
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
