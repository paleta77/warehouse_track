from django.contrib import admin
from .models import Delivery, Truck, Driver, Customer, Worker

# Register your models here.
admin.site.register(Delivery)
admin.site.register(Truck)
admin.site.register(Driver)
admin.site.register(Customer)
admin.site.register(Worker)