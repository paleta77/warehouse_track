from django import forms
from .models import Delivery, Worker, Package

class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = [
            "status",
            "delivery_number",
            "delivery_type",
            "date",
            "warehouse",
            "customer",
            "workers",
            "truck",
            "dock",
            "aisle",
            "driver",
            "packages",
        ]
        widgets = {
            "date": forms.TextInput(attrs={"id": "id_date"}),
            "workers": forms.CheckboxSelectMultiple(),
            "packages": forms.CheckboxSelectMultiple(), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        packages = None
        warehouse = None

        # get warehouse and packages from form data if available
        if self.data:
            warehouse = self.data.get("warehouse") or self.initial.get("warehouse")
            packages = self.data.getlist("packages")
        elif self.initial:
            warehouse = self.initial.get("warehouse")
            packages = self.initial.get("packages")

        if warehouse and packages:
            temp_delivery = Delivery(warehouse_id=warehouse)
            
            temp_delivery._prefetched_objects_cache = {}
            temp_delivery.packages = Package.objects.filter(pk__in=packages)
            best_dock = temp_delivery.select_best_dock()
            if best_dock:
                self.fields["dock"].initial = best_dock.pk

        # empty until the date is selected
        self.fields["workers"].queryset = Worker.objects.none()