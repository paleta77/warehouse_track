from django import forms
from .models import Delivery, Worker, Package, Customer
from datetime import datetime

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
            customer = self.data.get("customer")
            warehouse = int(warehouse)
            temp_delivery = Delivery(warehouse_id=warehouse, customer_id=customer)
            packages_qs = Package.objects.filter(pk__in=packages)
            best_dock = temp_delivery.select_best_dock(packages=packages_qs)
            if best_dock:
                self.fields["dock"].initial = best_dock.pk

        # Set workers queryset based on submitted date
        date_str = self.data.get("date") or self.initial.get("date")
        if date_str:
            try:
                selected_datetime = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                current_hour = selected_datetime.hour
                self.fields["workers"].queryset = Worker.objects.filter(
                    work_start_hour__lte=current_hour,
                    work_end_hour__gt=current_hour
                )
            except Exception:
                self.fields["workers"].queryset = Worker.objects.none()
        else:
            self.fields["workers"].queryset = Worker.objects.none()