from django.shortcuts import render
import json


def read_context_file():
    with open('my_geek_shop/static/my_geek_shop/context.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def render_products(request):
    content = read_context_file()
    context = {
        'title': content['products']['title'],
        'text': content['products']['text'],
        'menu_links': content['products']['menu_links'],
    }
    return render(request, 'mainapp/products.html', context)
