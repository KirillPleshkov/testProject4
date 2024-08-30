import stripe
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.conf import settings

from item.models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY
domain = settings.DOMAIN


class CreateCheckoutSessionView(View):
    def get(self, request, *args, item_id, **kwargs):
        item = get_object_or_404(Item, id=item_id)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "rub",
                        "unit_amount": item.price,
                        "product_data": {"name": item.name},
                    },
                    "quantity": 1,
                },
            ],
            metadata={"item_id": item_id},
            mode="payment",
            success_url=domain + "/success/",
            cancel_url=domain + "/cancel/",
        )
        return JsonResponse({"checkout_session_id": checkout_session.id})
