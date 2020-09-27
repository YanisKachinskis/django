import json
import os

from django.shortcuts import render
from mainapp.models import *
from myshop.settings import BASE_DIR


# Create your views here.


# похожие продукты на странице products.html
with open(os.path.join(BASE_DIR, 'static', 'exmp.json'), 'r') as f:
    data = json.load(f)
    related_products = data['related_products']


def main(request):
    slogan = 'Новый уровень комфорта. Отличные характеристики.'
    products_list = Product.objects.all()[:3]

    content = {
        'products_list': products_list,
        'slogan': slogan,
        'title': 'главная'
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None):
    links_menu = ProductCategory.objects.all()
    related_products_1 = Product.objects.filter(category_id=1)
    related_products_2 = Product.objects.filter(category_id=2)
    related_products_3 = Product.objects.filter(category_id=3)
    content = {
        'links_menu': links_menu,
        'title': 'продукты',
        'related_products_1': related_products_1,
        'related_products_2': related_products_2,
        'related_products_3': related_products_3,

    }
    print(pk)
    return render(request, 'mainapp/products.html', content)


def contact(request):

    shop_list = Shop.objects.all()
    content = {
        'title': 'контакты',
        'shop_list': shop_list
    }
    return render(request, 'mainapp/contact.html', content)
