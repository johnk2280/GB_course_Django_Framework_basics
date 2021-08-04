from django.shortcuts import render

from mainapp.models import ProductCategory, Product
from mainapp.views import get_page_content

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
    return render(request, 'my_geek_shop/index.html', context)


def render_contacts(request):
    context = get_page_content(page_name='contacts', user=request.user)
    return render(request, 'my_geek_shop/contacts.html', context)


def render_prod_description(request):
    context = get_page_content(page_name='prod_description', user=request.user)
    return render(request, 'my_geek_shop/prod_description.html', context)
