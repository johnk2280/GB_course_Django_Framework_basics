from django.shortcuts import render

from mainapp.models import ProductCategory, Product
from mainapp.views import get_page_content, get_same_products

from my_geek_shop.settings import STATICFILES_DIRS

import json
import os


def get_categories():
    return ProductCategory.objects.values()


def load_from_json(file):
    file_path = os.path.join(STATICFILES_DIRS[0], 'my_geek_shop', file)
    with open('my_geek_shop/static/my_geek_shop/context.json', 'r', encoding='utf-8') as f:
        return json.load(f)


# def get_page_data(page_name):
#     data = load_from_json('context.json')
#     return {
#         'title': data[page_name]['title'],
#         'text': data[page_name]['text'],
#         'menu_links': get_categories(),
#     }


def render_index(request):
    context = get_page_content(page_name='contacts', user=request.user)
    context['products'] = Product.objects.all()[:4]
    return render(request, 'my_geek_shop/index.html', context)


def render_contacts(request):
    context = get_page_content(page_name='contacts', user=request.user)
    return render(request, 'my_geek_shop/contacts.html', context)


def get_selected_product(pk):
    return Product.objects.get(pk=pk)


def render_prod_description(request, pk):
    context = get_page_content(page_name='prod_description', user=request.user)
    selected_product = get_selected_product(pk)
    context['selected_product'] = selected_product
    context['same_products'] = get_same_products(selected_product)
    return render(request, 'my_geek_shop/prod_description.html', context)


def render_hot_deal(request):
    context = get_page_content(page_name='hot_deal', user=request.user)
    return render(request, 'my_geek_shop/hot_deal.html', context)
