from django.contrib import admin
from .models import Warehouse, Aisle, PayloadArea, Dock


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("company", "country", "city", "street")


class AisleAdmin(admin.ModelAdmin):
    list_display = ("number", "warehouse")


class PayloadAreaAdmin(admin.ModelAdmin):
    list_display = ("number", "payload_type", "aisle")


class DockAdmin(admin.ModelAdmin):
    list_display = ("number", "warehouse")


# Register your models here.
admin.site.register(Warehouse, WarehouseAdmin)
admin.site.register(Aisle, AisleAdmin)
admin.site.register(PayloadArea, PayloadAreaAdmin)
admin.site.register(Dock, DockAdmin)
