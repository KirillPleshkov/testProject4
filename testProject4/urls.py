from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("item/", include("item.urls")),
    path("buy/", include("buy.urls")),
    path("order/", include("order.urls")),
]
