from django.shortcuts import render


def render_products(request):
    return render(request, 'mainapp/products.html')
