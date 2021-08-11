from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


def create_user(request):
    pass


@user_passes_test(lambda u: u.is_superuser)
def get_users(request):
    title = 'admin panel/users'
    users = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': title,
        'objects': users,
    }
    return render(request, 'adminapp/users.html', context)


def update_user(request, pk):
    pass


def delete_user(request, pk):
    pass


def create_category(request):
    pass


def get_categories(request):
    title = 'admin panel/categories'
    categories = ProductCategory.objects.all()
    context = {
        'title': title,
        'objects': categories,
    }
    return render(request, 'adminapp/categories.html', context)


def update_category(request, pk):
    pass


def delete_category(request, pk):
    pass


def create_product(request, pk):
    pass


def get_product(request, pk):
    pass


def get_products_by_category(request, pk):
    title = 'admin panel/products'
    category = get_object_or_404(ProductCategory, pk=pk)
    products = Product.objects.filter(category__pk=pk).order_by('name')
    context = {
        'title': title,
        'category': category,
        'objects': products,
    }
    return render(request, 'adminapp/products.html', context)


def update_product(request, pk):
    pass


def delete_product(request, pk):
    pass
