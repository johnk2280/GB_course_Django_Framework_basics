from django.urls import path
from basketapp.views import render_basket

app_name = 'basketapp'

urlpatterns = [
    path('', render_basket, name='basket'),

]
