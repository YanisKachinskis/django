from django.db import models


# Create your models here.

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='название категории')
    description = models.TextField(blank=True, verbose_name='описание категории')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'категория(ю)'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    image = models.ImageField(upload_to='products_images', blank=True)
    short_desc = models.CharField(max_length=128, verbose_name='краткое описание', blank=True)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='колличество на складе', default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')


class Shop(models.Model):
    city = models.CharField(verbose_name='город', max_length=64)
    phone = models.PositiveSmallIntegerField(verbose_name='телефон')
    email = models.CharField(verbose_name='адрес электронной почты', max_length=64)
    address = models.CharField(verbose_name='адрес', max_length=128)

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'

    def __str__(self):
        return self.city
