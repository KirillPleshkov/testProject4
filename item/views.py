from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.conf import settings

from item.models import Item


class ItemView(TemplateView):
    """View для отображения информации о товаре"""

    template_name = "item/item.html"

    def get_context_data(self, id: int, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(id=id, **kwargs)

        item = get_object_or_404(Item, id=id)
        context["title"] = item.name
        context["item"] = item
        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY
        return context
