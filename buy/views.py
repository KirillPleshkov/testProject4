from typing import Any

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from buy.services.stripe import (
    create_stripe_item_payment_session,
    create_stripe_order_payment_session,
)
from item.models import Item
from order.models import Order


class BuyItemView(View):
    """View для получения stripe checkout_session_id, необходимого для оплаты Item"""

    def get(self, request, *args, item_id: int, **kwargs) -> JsonResponse:
        item = get_object_or_404(Item, id=item_id)

        checkout_session_id = create_stripe_item_payment_session(
            item.id, item.name, item.price
        )
        return JsonResponse({"id": checkout_session_id})


class BuyOrderView(View):
    """View для получения stripe checkout_session_id, необходимого для оплаты Order"""

    def get(self, request, *args, order_id: int, **kwargs) -> JsonResponse:
        query_set = Order.objects.prefetch_related("items").select_related(
            "discount", "tax"
        )
        order = get_object_or_404(query_set, id=order_id)

        checkout_session_id = create_stripe_order_payment_session(order)
        return JsonResponse({"id": checkout_session_id})


class SuccessView(TemplateView):
    """View для отображения страницы об успешной оплате"""

    template_name = "buy/success.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(id=id, **kwargs)
        context["title"] = "Удачная покупка"
        return context


class CancelView(TemplateView):
    """View для отображения страницы об неуспешной оплате"""

    template_name = "buy/cancel.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(id=id, **kwargs)
        context["title"] = "Неудачная покупка"
        return context
