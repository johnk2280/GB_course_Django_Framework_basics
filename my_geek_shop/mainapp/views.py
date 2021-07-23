from django.shortcuts import render
import json


def read_context_file():
    with open('my_geek_shop/static/my_geek_shop/context.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def render_products(request):
    context = {
        'title': read_context_file()['products']['title'],
        'text': read_context_file()['products']['text'],
        'menu_links': read_context_file()['products']['menu_links'],
    }
    return render(request, 'mainapp/products.html', context)
