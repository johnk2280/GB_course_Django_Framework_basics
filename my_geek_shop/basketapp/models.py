from django.db import models
from django.conf import settings

from mainapp.models import Product
from ordersapp.models import OrderItem


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()

        super(BasketQuerySet, self).delete(*args, **kwargs)


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

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

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @property
    def get_product_total_cost(self):
        return self.product.price * self.quantity

    @property
    def get_basket_cost(self):
        return sum(product.get_product_total_cost for product in Basket.objects.filter(user=self.user))

    @property
    def get_products_quantity(self):
        return sum(product.quantity for product in Basket.objects.filter(user=self.user))

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity

        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)

