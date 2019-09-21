from django.db import models
from .shop import Shop


class Faq(models.Model):
    id = models.IntegerField
    question = models.TextField()
    answer = models.TextField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, db_column="shop_id")

    class Meta:
        db_table = "faq"
