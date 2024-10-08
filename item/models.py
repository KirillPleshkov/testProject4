from django.db import models


class Item(models.Model):
    """Модель товара"""

    name = models.CharField(max_length=255, unique=True, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="цена")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Item({self.name}, {self.description}, {self.price})"
