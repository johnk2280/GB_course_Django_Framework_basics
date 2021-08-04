from django.urls import path
from .views import render_products
# from .views import get_category

app_name = 'mainapp'

urlpatterns = [
    path('', render_products, name='index'),
    path('category/<int:pk>/', render_products, name='category'),
    path('product/<int:pk>', render_products, name='product'),
]
