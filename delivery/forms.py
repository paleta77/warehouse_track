from django import forms
from .models import Delivery, Worker

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
            "date": forms.TextInput(attrs={"id": "id_date"}),  # plain text input for Flatpickr
            "workers": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # empty until the date is selected
        self.fields["workers"].queryset = Worker.objects.none()