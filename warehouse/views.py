from .models import Warehouse, Aisle
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def warehouses(request):
    warehouses = Warehouse.objects.annotate(aisles_count=Count("aisle"))
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
