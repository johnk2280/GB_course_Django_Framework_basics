import os
import json
import csv
from random import shuffle

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import ProductCategory, Product, ProductsFile
from my_geek_shop.settings import STATICFILES_DIRS


def get_categories():
    return ProductCategory.objects.all()


def load_from_json(file):
    file_path = os.path.join(STATICFILES_DIRS[0], 'my_geek_shop', file)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_files_to_upload():
    return ProductsFile.objects.filter(is_uploaded=False)


def get_products_from_csv(file):
    with open(file.file.path, 'r', encoding='utf-16') as f_obj:
        file_reader = csv.DictReader(f_obj)
        for row in file_reader:
            yield row


def add_products():
    uploaded_files = get_files_to_upload()
    if uploaded_files:
        for file in uploaded_files:
            for product in get_products_from_csv(file):
                category_name = product['category']
                category = ProductCategory.objects.get(name=category_name)
                product['category'] = category
                added_product = Product(**product)
                added_product.save()

            file.is_uploaded = True
            file.save()


def get_page_data(page_name, user):
    data = load_from_json('context.json')
    return {
        'title': data[page_name]['title'],
        'text': data[page_name]['text'],
        'menu_links': get_categories(),
        'basket': get_basket(user)
    }


def get_basket(user):
    return Basket.objects.filter(user=user) if user.is_authenticated else []


def get_products_from_db(pk):
    if pk and pk != 0:
        return Product.objects.filter(category__pk=pk).order_by('-quantity')

    return Product.objects.all()


def render_products(request, pk=None):
    add_products()
    context = get_page_data(page_name='products', user=request.user)
    products = get_products_from_db(pk)
    category = get_object_or_404(ProductCategory, pk=pk) or {'name': 'ALL'}

    context['category'] = category
    context['products'] = products[:12]

    return render(request, 'mainapp/products.html', context)
