from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    price = models.IntegerField(verbose_name="цена")  # цена в копейках

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    @property
    def normal_price(self):
        return f"{self.price:.2f}"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Item({self.name}, {self.description}, {self.price})"
