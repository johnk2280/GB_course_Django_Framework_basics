from django.db import models
from django.conf import settings

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )
    added_at = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True,
    )

    @property
    def get_product_total_cost(self):
        return self.product.price * self.quantity

    @property
    def get_basket_cost(self):
        return sum(product.get_product_total_cost for product in Basket.objects.filter(user=self.user))

    @property
    def get_products_quantity(self):
        return sum(product.quantity for product in Basket.objects.filter(user=self.user))
