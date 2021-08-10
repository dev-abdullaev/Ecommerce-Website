from io import BytesIO

from django.core.files import File
from django.db import models
from PIL import Image
from vendor.models import Vendor


class Category(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ["ordering"]
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Item(models.Model):
    category = models.ForeignKey(Category, related_name="product", on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name="product", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="images/")
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return self.title
