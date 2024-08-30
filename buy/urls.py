from django.urls import path

from buy.views import CreateCheckoutSessionView, CancelView, SuccessView

urlpatterns = [
    path(
        "<int:item_id>/",
        CreateCheckoutSessionView.as_view(),
        name="create_checkout_session",
    ),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("success/", SuccessView.as_view(), name="success"),
]
