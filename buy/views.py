from typing import Any

import stripe
from django.core.exceptions import BadRequest
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView

from item.models import Item
from order.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
domain = settings.DOMAIN


class BuyItemView(View):
    def get(self, request, *args, item_id: int, **kwargs) -> JsonResponse:
        item = get_object_or_404(Item, id=item_id)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "rub",
                        "unit_amount": int(item.price * 100),
                        "product_data": {"name": item.name},
                    },
                    "quantity": 1,
                },
            ],
            metadata={"item_id": item_id},
            mode="payment",
            success_url=domain + "/buy/success/",
            cancel_url=domain + "/buy/cancel/",
        )
        return JsonResponse({"id": checkout_session.id})


class BuyOrderView(View):
    def get(self, request, *args, order_id: int, **kwargs) -> JsonResponse:
        order = get_object_or_404(Order.objects.prefetch_related("items"), id=order_id)

        tax_rate = stripe.TaxRate.create(  # Here
            display_name="Налог на что-то", percentage=10, inclusive=False
        )

        coupon = stripe.Coupon.create(
            duration="repeating",
            duration_in_months=3,
            percent_off=25.5,
        )

        items_to_stripe = [
            {
                "price_data": {
                    "currency": "rub",
                    "unit_amount": int(m2m_item.item.price * 100),
                    "product_data": {"name": m2m_item.item.name},
                },
                "quantity": m2m_item.count,
                "tax_rates": [tax_rate["id"]],
            }
            for m2m_item in order.orderitemm2m_set.all()
        ]

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=items_to_stripe,
            metadata={"order_id": order_id},
            mode="payment",
            success_url=domain + "/buy/success/",
            cancel_url=domain + "/buy/cancel/",
            discounts=[{"coupon": coupon["id"]}],
        )
        return JsonResponse({"id": checkout_session.id})


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
