from django.shortcuts import render

from mainapp.models import ProductCategory, Product, ProductsFile

import json
import csv


def get_categories():
    pass


def read_context_file():
    with open('my_geek_shop/static/my_geek_shop/context.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_files_to_upload():
    return ProductsFile.objects.filter(is_uploaded=False)


def get_products(file) -> csv.DictReader:
    with open(file.file.path, 'r', encoding='utf-16') as f_obj:
        file_reader = csv.DictReader(f_obj)
        for row in file_reader:
            yield row


def add_products():
    uploaded_files = get_files_to_upload()
    if uploaded_files:
        for file in uploaded_files:
            for product in get_products(file):
                added_product = Product(
                    name=product['name'],
                    short_description=product['short_description'],
                    img=product['img'],
                    description=product['description'],
                    price=float(product['price']),
                    quantity=int(product['quantity']),
                    category_id=int(product['category_id']),
                )
                added_product.save()

            file.is_uploaded = True
            file.save()


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
