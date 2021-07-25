from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(
        verbose_name='имя',
        max_length=64,
        unique=True,
        db_index=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        verbose_name='категория'
    )
    name = models.CharField(
        verbose_name='название продукта',
        max_length=128,
    )
    short_description = models.CharField(
        verbose_name='краткое описание',
        max_length=256,
        blank=True,
    )
    img = models.ImageField(
        upload_to='products_images',
        blank=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    price = models.DecimalField(
        verbose_name='стоимость',
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='остаток на складе',
        default=0,
    )

    def __str__(self):
        return f'{self.name} - {self.pk}'

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class ProductsFile(models.Model):
    name = models.CharField(
        verbose_name='имя',
        max_length=64,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    file = models.FileField(
        upload_to='product_files',
    )
    is_uploaded = models.BooleanField(
        verbose_name='данные загружены',
        default=False,
        db_index=True,
    )

    def __str__(self):
        return self.file