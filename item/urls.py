from django.urls import path

from item.views import ItemView

urlpatterns = [
    path("<int:id>/", ItemView.as_view(), name="item"),
]
