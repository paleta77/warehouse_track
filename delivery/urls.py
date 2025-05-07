from django.urls import path
from . import views

urlpatterns = [
    path("deliveries/", views.deliveries, name="deliveries"),
    path(
        "deliveries/<int:delivery_id>/",
        views.delivery_detail,
        name="delivery_detail",
    ),
    path(
        "packages/<int:package_id>/",
        views.package_detail,
        name="package_detail",
    ),
]