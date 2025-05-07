from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from .models import Delivery, Truck, Package, Driver, Package
from django.shortcuts import get_object_or_404

@login_required(login_url="/")
def deliveries(request):
    deliveries = Delivery.objects.all()
    template = loader.get_template("all_deliveries.html")
    context = {
        "deliveries": deliveries,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url="/")
def delivery_detail(request, delivery_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    truck = get_object_or_404(Truck, id=delivery.truck.id)
    packages = Package.objects.filter(truck=truck)
    driver = get_object_or_404(Driver, id=delivery.driver.id)
    template = loader.get_template("details_delivery.html")
    context = {
        "delivery": delivery,
        "truck": truck,
        "packages": packages,
        "driver": driver,
    }
    return HttpResponse(template.render(context, request))

@login_required(login_url="/")
def package_detail(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    template = loader.get_template("details_package.html")
    context = {
        "package": package,
    }
    return HttpResponse(template.render(context, request))