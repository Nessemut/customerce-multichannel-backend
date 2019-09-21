from django.db import models
from django.utils import timezone


class Shop(models.Model):
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

    @classmethod
    def create(cls, name):
        shop = cls(name=name)
        shop.app_enabled = False
        shop.panel_title = 'Contact us'
        shop.panel_color = '5ee4ff'
        shop.install_date = timezone.now()
        shop.save()
        return shop

    @classmethod
    def get(cls, name):
        return Shop.objects.get(name=name)

    class Meta:
        db_table = "shop"
