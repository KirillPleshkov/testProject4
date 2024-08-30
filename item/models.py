from django.db import models


class Item(models.Model):
    """Модель товара"""

    name = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    price = models.IntegerField(verbose_name="цена(в копейках)")  # цена в копейках

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    @property
    def normal_price(self) -> str:
        return f"{self.price:.2f}"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Item({self.name}, {self.description}, {self.price})"
