import os
import json
import csv
from random import shuffle, sample

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


def add_products_from_files():
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


def get_basket(user):
    return list(Basket.objects.filter(user=user)) if user.is_authenticated else []


def get_products_from_db_by(pk):
    if pk and pk != 0:
        return list(Product.objects.filter(category__pk=pk).order_by('-quantity'))

    return list(Product.objects.all())


def get_hot_deal():
    return sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    return list(Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk))[:3]


def get_products_category(pk):
    return get_object_or_404(ProductCategory, pk=pk) if pk and pk != 0 else {'name': 'ALL'}


def get_page_content(page_name, user):
    data = load_from_json('context.json')
    hot_product = get_hot_deal()
    return {
        'title': data[page_name]['title'],
        'text': data[page_name]['text'],
        'menu_links': get_categories(),
        'basket': get_basket(user),
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }


def render_products(request, pk=None, page=1):
    add_products_from_files()
    context = get_page_content(page_name='products', user=request.user)
    products = get_products_from_db_by(pk)
    shuffle(products)

    # TODO: Пагинатор на вкладке products довести до ума.
    #  Сайт падает при выборе всех категорий.

    # paginator = Paginator(products, 3)
    # try:
    #     products_paginator = paginator.page(page)
    # except PageNotAnInteger:
    #     products_paginator = paginator.page(1)
    # except EmptyPage:
    #     products_paginator = paginator.page(paginator.num_pages)

    context['category'] = get_products_category(pk)
    context['products'] = products[:12]
    # context['products'] = products_paginator

    return render(request, 'mainapp/products.html', context)
