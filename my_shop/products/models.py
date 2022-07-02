from ast import arg
from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    price = models.FloatField()
    decsription = models.TextField(blank=True)
    photo = models.ImageField(upload_to="images/%Y/%m/%d", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(to=Category, related_name="products", on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product_detail", args=[self.id])
