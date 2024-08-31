from django.contrib import admin

from order.models import Order, OrderItemM2M, Discount, Tax


class ItemsInline(admin.TabularInline):
    model = OrderItemM2M
    fields = ("order", "item", "count")
    autocomplete_fields = ("item",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (ItemsInline,)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    readonly_fields = ("stripe_id",)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    readonly_fields = ("stripe_id",)
