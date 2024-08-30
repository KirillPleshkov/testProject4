from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from item.models import Item


class ItemView(TemplateView):
    template_name = "item/item.html"

    def get_context_data(self, id, **kwargs):
        item = get_object_or_404(Item, id=id)
        context = super().get_context_data(id=id, **kwargs)
        context["title"] = item.name
        context["item"] = item
        return context
