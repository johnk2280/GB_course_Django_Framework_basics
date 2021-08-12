from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductEditForm


def create_user(request):
    title = 'users/create'

    if request.method == "POST":
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))

    user_form = ShopUserRegisterForm()
    context = {
        'title': title,
        'update_form': user_form,
    }
    return render(request, 'adminapp/update_user.html', context)


@user_passes_test(lambda u: u.is_superuser)
def get_users(request):
    title = 'admin panel/users'
    users = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': title,
        'objects': users,
    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def update_user(request, pk):
    title = 'users/update'
    edit_user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=[edit_user.pk])
        if edit_form.is_valid:
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:update_user', args=[edit_user.pk]))

    edit_form = ShopUserAdminEditForm(instance=edit_user)
    context = {
        'title': title,
        'update_form': edit_form,
    }
    return render(request, 'adminapp/update_user.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, pk):
    title = 'users/delete'
    user_to_delete = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_to_delete.is_active = False
        user_to_delete.save()
        return HttpResponseRedirect(reverse('admin:users'))

    context = {
        'title': title,
        'user_to_delete': user_to_delete,
    }
    return render(request, 'adminapp/delete_user.html', context)


@user_passes_test(lambda u: u.is_superuser)
def create_category(request):
    pass


@user_passes_test(lambda u: u.is_superuser)
def get_categories(request):
    title = 'admin panel/categories'
    categories = ProductCategory.objects.all()
    context = {
        'title': title,
        'objects': categories,
    }
    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def update_category(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, pk):
    pass


@user_passes_test(lambda u: u.is_superuser)
def create_product(request, pk):
    title = 'product/create'
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))

    product_form = ProductEditForm(initial={'category': category})
    context = {
        'title': title,
        'update_form': product_form,
        'category': category,
    }
    return render(request, 'admin: update_product.html', context)


@user_passes_test(lambda u: u.is_superuser)
def get_product(request, pk):
    title = 'product/more details'
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': title,
        'object': product,
    }
    return render(request, 'adminapp/product_description, content')


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
def update_product(request, pk):
    title = 'product/edit'
    edit_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:update_product'))

    edit_form = ProductEditForm(instance=edit_product)
    context = {
        'title': title,
        'update_form': edit_form,
        'category': edit_product.category,
    }
    return render(request, 'adminapp:update_product.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, pk):
    title = 'product/delete'
    product_to_delete = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_to_delete.is_active = False
        product_to_delete.save()
        return HttpResponseRedirect(reverse('admin:products', args=[product_to_delete.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product_to_delete,
    }
    return render(request, 'adminapp:delete_product.html', context)
