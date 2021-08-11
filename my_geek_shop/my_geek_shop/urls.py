"""my_geek_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import mainapp.views
from my_geek_shop.views import render_index, render_contacts, render_prod_description, render_hot_deal

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', render_index, name='index'),
    path('contacts/', render_contacts, name='contacts'),
    path('prod_description/<int:pk>', render_prod_description, name='prod_description'),
    path('hot_deal/', render_hot_deal, name='hot_deal'),
    path('products/', include('mainapp.urls', namespace='products'), name='products'),
    path('auth/', include('authapp.urls', namespace='auth'), name='auth'),
    path('basket/', include('basketapp.urls', namespace='basket'), name='basket'),
    path('admin/', include('adminapp.urls', namespace='admin'), name='admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
