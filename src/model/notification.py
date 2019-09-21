from django.db import models
from .shop import Shop


class Notification(models.Model):
    id = models.IntegerField
    background_color = models.CharField(max_length=6)
    font_color = models.CharField(max_length=6)
    text = models.TextField(max_length=6)
    time = models.IntegerField()
    url = models.CharField(max_length=2083)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column="shop_id")

    class Meta:
        db_table = "notification"
