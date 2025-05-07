from django import forms
from .models import Delivery

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
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "workers": forms.CheckboxSelectMultiple(),
        }