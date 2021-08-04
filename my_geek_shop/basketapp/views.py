from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product


def add_product_to_basket(request, pk):
    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_product_from_basket(request, pk):
    product = get_object_or_404(Basket, pk=pk)
    product.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_basket_content():
    pass


def render_basket(request):
    title = 'Корзина'
    text = 'products in the cart'
    basket_items = Basket.objects.filter(user=request.user).order_by('product__category')
    context = {
        'title': title,
        'text': text,
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/basket.html', context)
