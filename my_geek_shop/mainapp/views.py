from django.shortcuts import render

import os
import csv

from mainapp.models import ProductCategory, Product, ProductsFile

import json

from my_geek_shop.settings import BASE_DIR


def get_categories():
    return ProductCategory.objects.values()


def read_context_file():
    with open('my_geek_shop/static/my_geek_shop/context.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def check_file_upload():
    pass


def get_products_from_file(file):
    added_products = []
    file_path = os.path.join(BASE_DIR, 'media', file)
    with open(file_path, 'r', encoding='utf-16') as f_obj:
        file_reader = csv.DictReader(f_obj)
        for row in file_reader:
            added_products.append(row)

    # TODO: здесь реализовать через yield

    return added_products


def get_uploaded_products_files():
    uploaded_files = [
        file for file in sorted(ProductsFile.objects.values(), reverse=True) if file['is_uploaded'] == False
    ]
    # TODO: здесь реализовать выборку через query selectors
    return uploaded_files


def add_products():
    uploaded_files = get_uploaded_products_files()
    for file in uploaded_files:
        products = get_products_from_file(file['file'])
        for product in products:
            added_product = Product(
                name=product['name'],
                short_description=product['short_description'],
                img=product['img'],
                description=product['description'],
                price=product['price'],
                quantity=product['quantity'],
                category_id=product['category_id']
            )
            added_product.save()

        # TODO: здесь реализовать установки флага 'is_uploaded' в True


def get_page_data(page_name):
    data = read_context_file()
    # TODO: добавить данные в словарь и реализовать динамическое наполнение товарами
    return {
        'title': data[page_name]['title'],
        'text': data[page_name]['text'],
        'menu_links': get_categories(),

    }


def render_products(request):
    add_products()
    context = get_page_data('products')
    return render(request, 'mainapp/products.html', context)


def get_category(request, pk=None):
    # TODO: здесь реализовать обработку вызова категорий
    print(pk)
