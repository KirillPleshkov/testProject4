import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.conf import settings
from django.views.generic import TemplateView

from item.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY
domain = settings.DOMAIN


class CreateCheckoutSessionView(View):
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


class SuccessView(TemplateView):
    template_name = "buy/success.html"


class CancelView(TemplateView):
    template_name = "buy/cancel.html"
