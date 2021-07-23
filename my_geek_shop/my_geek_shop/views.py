from django.shortcuts import render
import json


def read_context_file():
    with open('static/my_geek_shop/context.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def render_index(request):
    return render(request, 'my_geek_shop/index.html')


def render_contacts(request):
    return render(request, 'my_geek_shop/contacts.html')


def render_prod_description(request):
    return render(request, 'my_geek_shop/prod_description.html')


# def render_header_menu(request):
#     context = {
#         'header_menu_links': read_context_file()['header_menu_links']
#     }
#     return render(request, 'my_geek_shop/includes/inc_header_menu.html', context)
