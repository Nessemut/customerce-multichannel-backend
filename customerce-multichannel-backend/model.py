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
    free_billing = models.BooleanField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_enabled = False
        self.panel_title = 'Contact us'
        self.panel_color = '5ee4ff'
        self.install_date = timezone.now()


class Notification(models.Model):
    id = models.IntegerField
    background_color = models.CharField(max_length=6)
    font_color = models.CharField(max_length=6)
    text = models.TextField(max_length=6)
    time = models.IntegerField()
    url = models.CharField(max_length=2083)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column="shop_id")


class Faq(models.Model):
    id = models.IntegerField
    question = models.TextField()
    answer = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column="shop_id")
