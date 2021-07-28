from django.contrib import admin

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product, ProductsFile

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductsFile)
admin.site.register(ShopUser)

