from typing import Any

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from buy.services.stripe import stripe_create_item, stripe_create_order
from item.models import Item
from order.models import Order


class BuyItemView(View):
    def get(self, request, *args, item_id: int, **kwargs) -> JsonResponse:
        item = get_object_or_404(Item, id=item_id)

        checkout_session_id = stripe_create_item(item.id, item.name, item.price)
        return JsonResponse({"id": checkout_session_id})


class BuyOrderView(View):
    def get(self, request, *args, order_id: int, **kwargs) -> JsonResponse:
        query_set = Order.objects.prefetch_related("items").select_related(
            "discount", "tax"
        )
        order = get_object_or_404(query_set, id=order_id)

        checkout_session_id = stripe_create_order(order)
        return JsonResponse({"id": checkout_session_id})


class SuccessView(TemplateView):
    template_name = "buy/success.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(id=id, **kwargs)
        context["title"] = "Удачная покупка"
        return context


class CancelView(TemplateView):
    template_name = "buy/cancel.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(id=id, **kwargs)
        context["title"] = "Неудачная покупка"
        return context
