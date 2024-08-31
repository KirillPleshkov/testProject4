from django.conf import settings
import stripe
from stripe import TaxRate

stripe.api_key = settings.STRIPE_SECRET_KEY

domain = settings.DOMAIN


def stripe_create_item(item_id: int, item_name: str, item_price) -> str:
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "rub",
                    "unit_amount": int(item_price * 100),
                    "product_data": {"name": item_name},
                },
                "quantity": 1,
            },
        ],
        metadata={"item_id": item_id},
        mode="payment",
        success_url=domain + "/buy/success/",
        cancel_url=domain + "/buy/cancel/",
    )

    return checkout_session.id


def stripe_create_order(order) -> str:
    discount = stripe_get_discount(order.discount.stripe_id)
    tax_rate = stripe_get_tax_rate(order.tax.stripe_id)

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
        metadata={"order_id": order.id},
        mode="payment",
        success_url=domain + "/buy/success/",
        cancel_url=domain + "/buy/cancel/",
        discounts=[{"coupon": discount["id"]}],
    )

    return checkout_session.id


def stripe_get_discount(coupon_id: str) -> stripe.Coupon | None:
    try:
        return stripe.Coupon.retrieve(coupon_id)
    except Exception:
        return None


def stripe_delete_discount(coupon_id: str) -> None:
    try:
        stripe.Coupon.delete(coupon_id)
    except Exception:
        return None


def stripe_create_discount(name: str, percentage: int) -> str:
    coupon = stripe.Coupon.create(
        name=name,
        percent_off=percentage,
        duration="forever",
    )
    return coupon["id"]


def stripe_save_or_update_discount(coupon_id: str, name: str, percentage: int) -> str:
    stripe_discount = stripe_get_discount(coupon_id)
    if stripe_discount is not None:
        stripe_delete_discount(stripe_discount["id"])

    return stripe_create_discount(name, percentage)


def stripe_get_tax_rate(tax_rate_id: str) -> TaxRate | None:
    try:
        return stripe.TaxRate.retrieve(tax_rate_id)
    except Exception:
        return None


def stripe_delete_tax_rate(tax_rate_id: str) -> None:
    try:
        stripe.TaxRate.modify(
            tax_rate_id,
            active=False,
        )
    except Exception:
        return None


def stripe_create_tax_rate(name: str, percentage: int) -> str:
    tax_rate = stripe.TaxRate.create(
        display_name=name,
        percentage=percentage,
        inclusive=False,
    )
    return tax_rate["id"]


def stripe_save_or_update_tax_rate(tax_rate_id: str, name: str, percentage: int) -> str:
    stripe_tax_rate = stripe_get_tax_rate(tax_rate_id)
    if stripe_tax_rate is not None:
        stripe_delete_tax_rate(stripe_tax_rate["id"])

    return stripe_create_tax_rate(name, percentage)
