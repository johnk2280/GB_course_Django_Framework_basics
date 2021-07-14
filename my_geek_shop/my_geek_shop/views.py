from django.shortcuts import render


def render_index(request):
    return render(request, 'my_geek_shop/index.html')


def render_contacts(request):
    return render(request, 'my_geek_shop/contacts.html')


def render_prod_description(request):
    return render(request, 'my_geek_shop/prod_description.html')