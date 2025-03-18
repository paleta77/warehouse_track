from django.contrib import admin
from .models import Warehouse

class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("company", "country", "city", "street")
    
# Register your models here.
admin.site.register(Warehouse, WarehouseAdmin)