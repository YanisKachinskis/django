import json
import os
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import *


# def get_basket(user):
#     if user.is_authenticated:
#         return Basket.objects.filter(user=user)
#     return []


def get_hot_product():
    products_list = Product.objects.filter(is_active=True, category__is_active=True)
    return random.sample(list(products_list), 1)[0]


def get_related_products(hot_product):
    related_products = Product.objects.filter(category_id=hot_product.category_id).exclude(pk=hot_product.pk).exclude(
        is_active=False)[:3]
    return related_products


def main(request):
    slogan = 'Новый уровень комфорта. Отличные характеристики.'

    content = {
        'slogan': slogan,
        'title': 'главная',
        'products_list': Product.objects.all()[:3]
    }
    return render(request, 'mainapp/index.html', content)


def products(request, pk=None, page=1):
    links_menu = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            all_products = Product.objects.filter(is_active=True, category__is_active=True)
            category = {
                'pk': 0,
                'name': 'все'
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            all_products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')

        paginator = Paginator(all_products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'links_menu': links_menu,
            'title': 'продукты',
            'products': products_paginator,
            'category': category,
        }

        return render(request, 'mainapp/product_list.html', content)

    hot_product = get_hot_product()
    related_products = get_related_products(hot_product)

    content = {
        'links_menu': links_menu,
        'title': 'продукты',
        'hot_product': hot_product,
        'related_products': related_products,
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    shop_list = Shop.objects.all()
    content = {
        'title': 'контакты',
        'shop_list': shop_list,
    }
    return render(request, 'mainapp/contact.html', content)


def product(request, pk):
    product_item = get_object_or_404(Product, pk=pk)
    links_menu = ProductCategory.objects.all()

    content = {
        'product': product_item,
        'title': 'товар',
        'links_menu': links_menu,
        'related_products': get_related_products(product_item)
    }
    return render(request, 'mainapp/product.html', content)
