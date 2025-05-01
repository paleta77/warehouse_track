from django.urls import path
from . import views

urlpatterns = [
    path("deliveries/", views.deliveries, name="deliveries"),
    path(
        "deliveries/<int:delivery_id>/",
        views.delivery_detail,
        name="delivery_detail",
    ),
]