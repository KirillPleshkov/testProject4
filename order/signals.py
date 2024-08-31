from django.db.models.signals import post_delete
from django.dispatch import receiver

from buy.services.stripe import stripe_delete_discount, stripe_delete_tax_rate
from order.models import Discount, Tax


@receiver(post_delete, sender=Discount)
def post_delete_discount(instance, **kwargs):
    stripe_delete_discount(instance.stripe_id)


@receiver(post_delete, sender=Tax)
def post_delete_tax_rate(instance, **kwargs):
    stripe_delete_tax_rate(instance.stripe_id)
