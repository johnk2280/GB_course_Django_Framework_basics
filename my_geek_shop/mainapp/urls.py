from django.urls import path
from .views import render_products, get_category

app_name = 'mainapp'

urlpatterns = [
    path('', render_products, name='index'),
    path('<int:pk>/', get_category, name='category')
]
