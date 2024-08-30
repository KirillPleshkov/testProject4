from django.urls import path

from buy.views import CreateCheckoutSessionView

urlpatterns = [
    path(
        "<int:item_id>/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    )
]
