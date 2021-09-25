from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductEditForm, ProductCategoryEditForm


class UserCreateView(CreateView):
    model = ShopUser
    template_name = 'adminapp/update_user.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'users/create'
        context['header'] = 'user'
        context['table_header'] = 'creation'
        return context


class UserListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'admin panel/users'
        context['header'] = 'Users'
        context['table_header'] = 'Users'
        return context


class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/update_user.html'
    success_url = reverse_lazy('admin:users')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'users/update'
        context['header'] = 'user'
        context['table_header'] = 'update'
        return context


class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/delete_user.html'
    success_url = 'admin:users'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(reverse(self.get_success_url()))

    def get_context_data(self, **kwargs):
        context = super(UserDeleteView, self).get_context_data(**kwargs)
        context['title'] = 'users/delete'
        return context


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/update_category.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductCategoryCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'categories/create'
        context['header'] = 'category'
        context['table_header'] = 'creation'
        return context


class ProductCategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ProductCategoryListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return ProductCategory.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'admin panel/categories'
        context['header'] = 'categories'
        context['table_header'] = 'categories'
        return context


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/update_category.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'category/edit'
        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/delete_category.html'
    success_url = 'admin:categories'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(reverse(self.get_success_url()))


# TODO: При добавлении картинки, при создании товара, в базу записывается полный путь от папки /media/.
#  Должно записываться имя файла.
#  При загрузке картинки на странице, необходимо джойнить путь до картинки с учетом всех поддерикторий /media/.
#  TODO: перевести products на CBV.

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
    return render(request, 'adminapp/update_product.html', context)


@user_passes_test(lambda u: u.is_superuser)
def get_product(request, pk):
    title = 'product/more details'
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': title,
        'object': product,
    }
    return render(request, 'adminapp/product_description.html', context)


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
    editable_product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=editable_product)
        if edit_form.is_valid():
            editable_product.is_active = True
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[editable_product.category.pk]))

    edit_form = ProductEditForm(instance=editable_product)
    context = {
        'title': title,
        'update_form': edit_form,
        'category': editable_product.category,
    }
    return render(request, 'adminapp/update_product.html', context)


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
    return render(request, 'adminapp/delete_product.html', context)
