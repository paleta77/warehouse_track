import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from delivery.models import Delivery, Worker

@login_required(login_url="/")
def dashboard(request):
    deliveries_upcoming = Delivery.objects.filter(date__gt=datetime.datetime.now()).order_by("date")[:10]
    workers = Worker.objects.filter(
        work_start_hour__lt=datetime.datetime.now().time().hour,
        work_end_hour__gt=datetime.datetime.now().time().hour,
    )
    deliveries_at_dock = Delivery.objects.filter(status="at_dock")
    return render(request, "dashboard.html", {
        "deliveries_upcoming": deliveries_upcoming,
        "workers": workers,
        "deliveries_at_dock": deliveries_at_dock,
    })
