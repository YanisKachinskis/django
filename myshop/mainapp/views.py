import json
import os

from django.shortcuts import render

from myshop.settings import BASE_DIR

# Create your views here.
links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]

# похожие продукты на странице products.html
with open(os.path.join(BASE_DIR, 'static', 'exmp.json'), 'r') as f:
    data = json.load(f)
    related_products = data['related_products']


slogan = 'Новый уровень комфорта. Отличные характеристики.'


def main(request):
    content = {
        'slogan': slogan,
        'title': 'главная'
    }
    return render(request, 'mainapp/index.html', content)


def products(request):
    content = {
        'links_menu': links_menu,
        'title': 'продукты',
        'related_products': related_products
    }
    return render(request, 'mainapp/products.html', content)


def contact(request):
    content = {
        'title': 'контакты'
    }
    return render(request, 'mainapp/contact.html', content)