from django.contrib import admin
from .models import Delivery, Truck, Driver, Customer, Worker

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ("delivery_number", "delivery_type", "date", "warehouse", "customer")
    
class TruckAdmin(admin.ModelAdmin):
    list_display = ("registration_plates", "brand")
    
class DriverAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "telephone", "email")
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "telephone", "email")

class WorkerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "telephone", "email", "company", "work_start_hour", "work_end_hour")

# Register your models here.
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Worker, WorkerAdmin)