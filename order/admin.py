from django.contrib import admin

from order.models import Order, OrderItemM2M


class ItemsInline(admin.TabularInline):
    model = OrderItemM2M
    fields = ("order", "item", "count")
    autocomplete_fields = ("item",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (ItemsInline,)
