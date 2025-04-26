from .models import Warehouse, Aisle, PayloadArea, Dock
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def warehouses(request):
    warehouses = Warehouse.objects.annotate(
        aisles_count=Count("aisle"), docks_count=Count("dock")
    )
    template = loader.get_template("all_warehouses.html")
    context = {
        "warehouses": warehouses,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/")
def warehouse_detail(request, warehouse_id):
    warehouse = Warehouse.objects.get(id=warehouse_id)
    aisles_count = Aisle.objects.filter(warehouse=warehouse).count()
    template = loader.get_template("details_warehouse.html")
    context = {
        "warehouse": warehouse,
        "aisles_count": aisles_count,
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url="/")
def aisles_of_warehouse(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    aisles = Aisle.objects.filter(warehouse=warehouse)
    return render(
        request, "all_aisles.html", {"warehouse": warehouse, "aisles": aisles}
    )


@login_required(login_url="/")
def payload_areas_of_aisle(request, aisle_id):
    aisle = get_object_or_404(Aisle, id=aisle_id)
    payload_areas = PayloadArea.objects.filter(aisle=aisle)
    return render(
        request,
        "all_payload_areas.html",
        {"aisle": aisle, "payload_areas": payload_areas},
    )


@login_required(login_url="/")
def docks_of_warehouse(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    docks = Dock.objects.filter(warehouse=warehouse)
    return render(request, "all_docks.html", {"warehouse": warehouse, "docks": docks})
