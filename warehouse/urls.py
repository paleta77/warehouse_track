from django.urls import path
from . import views


urlpatterns = [
    path("warehouses/", views.warehouses, name="warehouses"),
    path(
        "warehouses/<int:warehouse_id>/",
        views.warehouse_detail,
        name="warehouse_detail",
    ),
]
