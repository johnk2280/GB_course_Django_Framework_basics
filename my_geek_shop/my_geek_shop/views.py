from django.shortcuts import render

from mainapp.models import ProductCategory, Product

import json


def get_categories():
    return ProductCategory.objects.values()


def read_context_file():
    with open('my_geek_shop/static/my_geek_shop/context.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_page_data(page_name):
    data = read_context_file()
    return {
        'title': data[page_name]['title'],
        'text': data[page_name]['text'],
        'menu_links': get_categories(),
    }


def render_index(request):
    return render(request, 'my_geek_shop/index.html')


def render_contacts(request):
    context = get_page_data('contacts')
    return render(request, 'my_geek_shop/contacts.html', context)


def render_prod_description(request):
    context = get_page_data('prod_description')
    return render(request, 'my_geek_shop/prod_description.html', context)
