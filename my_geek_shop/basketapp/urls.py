from django.urls import path
from basketapp.views import render_basket, add_product_to_basket, remove_product_from_basket

app_name = 'basketapp'

urlpatterns = [
    path('', render_basket, name='basket'),
    path('add/<int:pk>/', add_product_to_basket, name='add'),
    path('remove/<int:pk>/', remove_product_from_basket, name='remove'),
]
