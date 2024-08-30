from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="цена")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Item({self.name}, {self.description}, {self.price})"
