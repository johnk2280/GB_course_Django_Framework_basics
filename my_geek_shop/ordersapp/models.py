from django.db import models
from django.conf import settings
from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'formed'),
        (SENT_TO_PROCEED, 'sent for processing'),
        (PAID, 'paid'),
        (PROCEEDED, 'processed'),
        (READY, 'ready'),
        (CANCEL, 'canceled'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        verbose_name='создан',
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name='обновлен',
        auto_now=True,
    )
    status = models.CharField(
        verbose_name='статус',
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING,
    )
    is_active = models.BooleanField(
        verbose_name='активен',
        default=True,
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Current order {self.id}'

    def get_items(self):
        return self.orderitems.select_related()

    def get_total_quantity(self):
        return sum(list(map(lambda x: x.quantity, self.get_items())))

    def get_product_type_quantity(self):
        return len(self.get_items())

    def get_total_cost(self):
        return sum(list(map(lambda x: x.quantity * x.product.price, self.get_items())))

    def delete(self):
        for item in self.get_items():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItemQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()

        super(OrderItemQuerySet, self).delete(*args, **kwargs)


class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(
        Order,
        related_name='orderitems',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='продукт',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first()
