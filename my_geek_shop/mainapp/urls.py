from django.urls import path
from .views import render_products

urlpatterns = [
    path('', render_products),
]
