from .models import Warehouse
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/")
def warehouses(request):
    warehouses = Warehouse.objects.all()
    template = loader.get_template("all_warehouses.html")
    context = {
        "warehouses": warehouses,
    }
    return HttpResponse(template.render(context, request))


def warehouse_detail(request, warehouse_id):
    warehouse = Warehouse.objects.get(id=warehouse_id)
    template = loader.get_template("details_warehouse.html")
    context = {
        "warehouse": warehouse,
    }
    return HttpResponse(template.render(context, request))
