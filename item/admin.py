from django.contrib import admin

from item.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin): ...
