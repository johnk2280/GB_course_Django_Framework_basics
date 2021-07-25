from django.shortcuts import render

from mainapp.models import ProductCategory, Product, ProductsFile

import json


def get_categories():
    return ProductCategory.objects.values()


def read_context_file():
    with open('my_geek_shop/static/my_geek_shop/context.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def check_file_upload():
    pass


def read_products_file():
    pass


def upload_products_file():
    uploaded_files = [
        file for file in sorted(ProductsFile.objects.values(), reverse=True) if file['is_uploaded'] == False
    ]
    return uploaded_files


def get_page_data(page_name):
    data = read_context_file()
    return {
        'title': data[page_name]['title'],
        'text': data[page_name]['text'],
        'menu_links': get_categories(),

    }


def render_products(request):
    print(upload_products_file())
    context = get_page_data('products')
    return render(request, 'mainapp/products.html', context)


def get_category(request, pk=None):
    print(pk)
