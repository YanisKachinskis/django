import json
import os

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import *
from myshop.settings import BASE_DIR


# Create your views here.


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

    baskets = Basket.objects.filter(user=request.user)
    basket_quantity = Basket.objects.filter(user=request.user).values('quantity')

    final_price = 0
    for basket in baskets:
        final_price += (Product.objects.get(id=basket.__dict__['product_id']).__dict__['price'] * basket.__dict__['quantity'])

    sum_bask = 0
    for item in list(basket_quantity):
        sum_bask = sum_bask + item['quantity']

    if pk is not None:
        if pk == 0:
            all_products = Product.objects.all()
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            all_products = Product.objects.filter(category__pk=pk).order_by('price')

        content = {
            'links_menu': links_menu,
            'title': 'продукты',
            'products': all_products,
            'category': category,
            'basket': baskets,
            'sum_bask': sum_bask,
            'final_price': final_price
        }

        return render(request, 'mainapp/product_list.html', content)
    related_products = Product.objects.filter(price__lt=4000).order_by('price')[:3]
    content = {
        'links_menu': links_menu,
        'title': 'продукты',
        'related_products': related_products,
        'basket': baskets,
        'sum_bask': sum_bask,
        'final_price': final_price
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    shop_list = Shop.objects.all()
    content = {
        'title': 'контакты',
        'shop_list': shop_list
    }
    return render(request, 'mainapp/contact.html', content)
