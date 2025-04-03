from django.db import models
from companies.models import Company


# Create your models here.
class Warehouse(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building_number = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"Warehouse: {self.company} - {self.city}, {self.street}"


class Dock(models.Model):
    number = models.IntegerField(unique=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f"Dock: {self.number} - {self.warehouse}"


class Aisle(models.Model):
    number = models.IntegerField(unique=True)
    length = models.IntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f"Aisle: {self.number} - {self.warehouse}"


PAYLOAD_TYPES = {
    "food": "Food",
    "drinks": "Drinks",
    "rtv": "RTV",
    "agd": "AGD",
    "electronics": "Electronics",
    "other": "Other",
}


class PayloadArea(models.Model):
    number = models.IntegerField(unique=True)
    payload_type = models.CharField(
        max_length=50, choices=PAYLOAD_TYPES, default="other"
    )
    aisle = models.ForeignKey(Aisle, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payload area: {self.number} in {self.aisle}"
