from typing import Any

from django.conf import settings
import stripe
from stripe import TaxRate

stripe.api_key = settings.STRIPE_SECRET_KEY

domain = settings.DOMAIN


def _get_stripe_checkout_session_id(
    items: list[dict[str, Any]], metadata_id: int, discount: str | None = None
):
    """Создание stripe checkout Session"""
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=items,
        metadata={"id": metadata_id},
        mode="payment",
        success_url=domain + "/buy/success/",
        cancel_url=domain + "/buy/cancel/",
        discounts=[{"coupon": discount}],
    )

    return checkout_session.id


def create_stripe_item_payment_session(item_id: int, item_name: str, item_price) -> str:
    """Создание stripe checkout Session для покупки Item"""
    items = [
        {
            "price_data": {
                "currency": "rub",
                "unit_amount": int(item_price * 100),
                "product_data": {"name": item_name},
            },
            "quantity": 1,
        },
    ]
    return _get_stripe_checkout_session_id(items, item_id)


def create_stripe_order_payment_session(order) -> str:
    """Создание stripe checkout Session для покупки Order с указанием скидки и налога"""
    discount = get_stripe_discount(order.discount.stripe_id)
    tax_rate = get_stripe_tax_rate(order.tax.stripe_id)

    items = [
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

    return _get_stripe_checkout_session_id(items, order.id, discount)


def get_stripe_discount(coupon_id: str) -> stripe.Coupon | None:
    """Получение stripe Coupon по id"""
    try:
        return stripe.Coupon.retrieve(coupon_id)
    except Exception:
        return None


def delete_stripe_discount(coupon_id: str) -> None:
    """Удаление stripe Coupon по id"""
    try:
        stripe.Coupon.delete(coupon_id)
    except Exception:
        return None


def create_stripe_discount(name: str, percentage: int) -> str:
    """Создание stripe Coupon по name и percentage"""
    coupon = stripe.Coupon.create(
        name=name,
        percent_off=percentage,
        duration="forever",
    )
    return coupon["id"]


def save_or_update_stripe_discount(coupon_id: str, name: str, percentage: int) -> str:
    """Создание stripe Coupon или удаление имеющегося и после создание измененного"""
    stripe_discount = get_stripe_discount(coupon_id)
    if stripe_discount is not None:
        delete_stripe_discount(stripe_discount["id"])

    return create_stripe_discount(name, percentage)


def get_stripe_tax_rate(tax_rate_id: str) -> TaxRate | None:
    """Получение stripe Tax rate"""
    try:
        return stripe.TaxRate.retrieve(tax_rate_id)
    except Exception:
        return None


def delete_stripe_tax_rate(tax_rate_id: str) -> None:
    """Удаление stripe Tax rate"""
    try:
        stripe.TaxRate.modify(
            tax_rate_id,
            active=False,
        )
    except Exception:
        return None


def create_stripe_tax_rate(name: str, percentage: int) -> str:
    """Создание stripe Tax rate"""
    tax_rate = stripe.TaxRate.create(
        display_name=name,
        percentage=percentage,
        inclusive=False,
    )
    return tax_rate["id"]


def save_or_update_stripe_tax_rate(tax_rate_id: str, name: str, percentage: int) -> str:
    """Создание stripe Tax rate или удаление имеющегося и после создание измененного"""
    stripe_tax_rate = get_stripe_tax_rate(tax_rate_id)
    if stripe_tax_rate is not None:
        delete_stripe_tax_rate(stripe_tax_rate["id"])

    return create_stripe_tax_rate(name, percentage)
