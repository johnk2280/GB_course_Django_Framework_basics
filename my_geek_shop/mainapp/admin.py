from django.contrib import admin

from mainapp.models import ProductCategory, Product, ProductsFile

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(ProductsFile)

