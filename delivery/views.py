from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from .models import Delivery, Truck, Driver, Package, Worker, Customer
from django.shortcuts import get_object_or_404, render, redirect
from .forms import DeliveryForm
from datetime import datetime

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

def create_delivery(request):
    if request.method == "POST":
        form = DeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("deliveries")
    else:
        form = DeliveryForm()
    return render(request, "add_delivery.html", {"form": form})

def get_available_workers(request):
    selected_date = request.GET.get("date")
    if selected_date:
        try:
            selected_datetime = datetime.strptime(selected_date, "%Y-%m-%d %H:%M")
            current_hour = selected_datetime.hour

            workers = Worker.objects.filter(
                work_start_hour__lte=current_hour,
                work_end_hour__gt=current_hour
            )

            workers_data = [{"id": worker.id, "name": f"{worker.first_name} {worker.last_name}"} for worker in workers]
            return JsonResponse({"workers": workers_data})
        except ValueError:
            return JsonResponse({"workers": []})
    return JsonResponse({"workers": []})

def get_best_dock(request):
    warehouse_id = request.GET.get("warehouse")
    package_ids = request.GET.getlist("packages[]")

    if warehouse_id and package_ids:
        customer = Customer.objects.first()  # Use any valid customer
        temp_delivery = Delivery(warehouse_id=warehouse_id, customer=customer)
        packages_qs = Package.objects.filter(pk__in=package_ids)
        best_dock = temp_delivery.select_best_dock(packages=packages_qs)
        return JsonResponse({"dock": best_dock.pk if best_dock else None})
    return JsonResponse({"dock": None})