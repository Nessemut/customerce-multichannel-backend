from django import forms
from ..model.shop import Shop


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = "__all__"
