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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def get_basket_cost(self, request):
        pass

    @property
    def get_products_quantity(self, request):
        return sum(product.quantity for product in self.objects.filter(user=request.user))

