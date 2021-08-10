from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string

from basketapp.models import Basket
from mainapp.models import Product


@login_required
def add_product_to_basket(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('prod_description', args=[pk]))

    product = get_object_or_404(Product, pk=pk)
    basket = Basket.objects.filter(user=request.user, product=product).first()
    if not basket:
        basket = Basket(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_basket_product(request, pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        product = Basket.objects.get(pk=int(pk))
        if quantity > 0:
            product.quantity = quantity
            product.save()
        else:
            product.delete()

        basket_items = Basket.objects.filter(user=request.user)

        context = {
            'basket_items': basket_items,
        }

        updated_basket_string = render_to_string(
            'basketapp/includes/inc_basket_list.html',
            context
        )

        return JsonResponse({'result': updated_basket_string})


@login_required
def remove_product_from_basket(request, pk):
    product = get_object_or_404(Basket, pk=pk)
    product.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_basket_content():
    pass


@login_required
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
