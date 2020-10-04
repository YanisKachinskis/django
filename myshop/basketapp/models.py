from django.conf import settings
from django.db import models

# Create your models here.

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')

    add_datetime = models.DateTimeField(auto_now_add=True)
