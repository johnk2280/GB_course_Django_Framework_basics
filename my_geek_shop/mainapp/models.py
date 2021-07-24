from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
