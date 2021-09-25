from django.urls import path

from adminapp.views import (
    # create_user,
    # get_users,
    # update_user,
    # delete_user,
    # create_category,
    # get_categories,
    # update_category,
    # delete_category,
    create_product, get_product,
    get_products_by_category,
    update_product,
    delete_product,

    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,

    ProductCategoryListView,
    ProductCategoryCreateView,
    ProductCategoryUpdateView,
    ProductCategoryDeleteView,

)

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', UserCreateView.as_view(), name='create_user'),
    path('users/read/', UserListView.as_view(), name='users'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='update_user'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),

    path('categories/create/', ProductCategoryCreateView.as_view(), name='create_category'),
    path('categories/read/', ProductCategoryListView.as_view(), name='categories'),
    path('categories/update/<int:pk>/', ProductCategoryUpdateView.as_view(), name='update_category'),
    path('categories/delete/<int:pk>/', ProductCategoryDeleteView.as_view(), name='delete_category'),

    path('products/create/category/<int:pk>/', create_product, name='create_product'),
    path('products/read/<int:pk>', get_product, name='product'),
    path('products/read/category/<int:pk>', get_products_by_category, name='products'),
    path('products/update/<int:pk>/', update_product, name='update_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),
]
