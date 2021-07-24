from django.shortcuts import render
import json


def read_context_file():
    with open('my_geek_shop/static/my_geek_shop/context.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_page_data(page_name):
    data = read_context_file()
    return {
        'title': data[page_name]['title'],
        'text': data[page_name]['text'],
        'menu_links': data[page_name]['menu_links'],
    }


def render_products(request):
    context = get_page_data('products')
    return render(request, 'mainapp/products.html', context)
