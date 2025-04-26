from django.urls import path
from . import views


urlpatterns = [
    path("warehouses/", views.warehouses, name="warehouses"),
    path(
        "warehouses/<int:warehouse_id>/",
        views.warehouse_detail,
        name="warehouse_detail",
    ),
    path(
        "warehouses/<int:warehouse_id>/aisles/",
        views.aisles_of_warehouse,
        name="aisles_of_warehouse",
    ),
    path(
        "aisles/<int:aisle_id>/payload_areas/",
        views.payload_areas_of_aisle,
        name="payload_areas_of_aisle",
    ),
    path(
        "warehouses/<int:warehouse_id>/docks/",
        views.docks_of_warehouse,
        name="docks_of_warehouse",
    ),
]
