from django import forms
from django.forms import ModelForm
from django.forms.fields import IntegerField

from items.models import Item


class ItemModelForm(ModelForm):
    class Meta:
        model = Item
        fields = ["category", "title", "price", "description", "image"]


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()
