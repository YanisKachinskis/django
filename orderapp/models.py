from django.conf import settings
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RD'
    CANCEL = 'CNC'

    ORDER_STATUSES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PAID, 'оплачен'),
        (PROCEEDED, 'обрабатывается'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    status = models.CharField(max_length=3, choices=ORDER_STATUSES, verbose_name='Статус', default=FORMING)
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Текущий заказ: #{self.id}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


# class OrderItemQuerySet(models.QuerySet):
#
#     def delete(self, *args, **kwargs):
#         for object in self:
#             object.product.quantity += object.quantity
#             object.product.save()
#         super(OrderItemQuerySet, self).delete()


class OrderItem(models.Model):
    #object = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(Order, related_name='orderitems', on_delete=models.CASCADE, verbose_name='заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.get(pk=pk)

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()



