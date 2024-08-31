from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.conf import settings

from order.models import Order


class OrderView(TemplateView):
    """View для отображения информации о заказе"""

    template_name = "order/order.html"

    def get_context_data(self, id: int, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(id=id, **kwargs)

        order = get_object_or_404(Order.objects.prefetch_related("items"), id=id)
        context["title"] = order.name
        context["order"] = order
        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY
        return context
