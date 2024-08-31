from django.core.validators import MinValueValidator
from django.db import models

from item.models import Item


class Order(models.Model):
    """Модель заказа объединяющая Items"""

    name = models.CharField(max_length=255, verbose_name="название")
    items = models.ManyToManyField(Item, through="OrderItemM2M")

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Order({self.name})"


class OrderItemM2M(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="заказ")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="товар")
    count = models.PositiveIntegerField(
        verbose_name="количество",
        validators=[MinValueValidator(1)],
    )

    class Meta:
        verbose_name = "товар заказа"
        verbose_name_plural = "товары заказа"
        unique_together = ("order", "item")

    def __str__(self):
        return f"Заказ: {self.order}, товар: {self.item}"
