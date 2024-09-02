from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from buy.services.stripe import (
    save_or_update_stripe_discount,
    save_or_update_stripe_tax_rate,
)
from item.models import Item


class Order(models.Model):
    """Модель заказа объединяющая Items"""

    name = models.CharField(max_length=255, verbose_name="название")
    items = models.ManyToManyField(Item, through="OrderItemM2M")

    discount = models.ForeignKey(
        "Discount",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="order",
        verbose_name="скидка",
    )
    tax = models.ForeignKey(
        "Tax",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="order",
        verbose_name="налог",
    )

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Order({self.name})"


class OrderItemM2M(models.Model):
    """Модель для связи Item и Order для хранения товаров заказа и их количества"""

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

    def __str__(self) -> str:
        return f"Заказ: {self.order}, товар: {self.item}"


class Discount(models.Model):
    """Модель скидки для заказа"""

    name = models.CharField(max_length=255, verbose_name="название")
    percentage = models.PositiveIntegerField(
        verbose_name="процент скидки",
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    stripe_id = models.CharField(
        max_length=255, blank=True, unique=True, null=True, verbose_name="stripe_id"
    )

    def save(self, *args, **kwargs):
        self.stripe_id = save_or_update_stripe_discount(
            self.stripe_id, self.name, self.percentage
        )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "скидка"
        verbose_name_plural = "скидки"

    def __str__(self) -> str:
        return self.name


class Tax(models.Model):
    """Модель налога для заказа"""

    name = models.CharField(max_length=255, verbose_name="название")
    percentage = models.PositiveIntegerField(
        verbose_name="процент налога",
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    stripe_id = models.CharField(
        max_length=255, blank=True, null=True, unique=True, verbose_name="stripe_id"
    )

    def save(self, *args, **kwargs):
        self.stripe_id = save_or_update_stripe_tax_rate(
            self.stripe_id, self.name, self.percentage
        )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "налог"
        verbose_name_plural = "налоги"

    def __str__(self) -> str:
        return self.name
