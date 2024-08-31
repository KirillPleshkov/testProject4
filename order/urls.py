from django.urls import path

from order.views import OrderView

urlpatterns = [
    path("<int:id>/", OrderView.as_view(), name="order"),
]
