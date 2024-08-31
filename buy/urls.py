from django.urls import path

from buy.views import BuyItemView, BuyOrderView, CancelView, SuccessView

urlpatterns = [
    path(
        "<int:item_id>/",
        BuyItemView.as_view(),
        name="buy-item",
    ),
    path(
        "order/<int:order_id>/",
        BuyOrderView.as_view(),
        name="buy-order",
    ),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("success/", SuccessView.as_view(), name="success"),
]
