from django.db import models
from warehouse.models import PayloadArea, Dock, Aisle, Warehouse
from companies.models import Company
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Truck(models.Model):
    registration_plates = models.CharField(max_length=15)
    brand = models.CharField(max_length=255)

class Driver(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = PhoneNumberField()
    email = models.EmailField(max_length=255)
    trucks = models.ManyToManyField(Truck)
    
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = PhoneNumberField()
    email = models.EmailField(max_length=255)
    
class Worker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = PhoneNumberField()
    email = models.EmailField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    work_start = models.TimeField()
    work_end = models.TimeField()
    
DELIVERY_TYPES = {
    "IN": "In",
    "OUT": "Out"
}

class Delivery(models.Model):
    delivery_number = models.CharField(max_length=255)
    delivery_type = models.CharField(max_length=255, choices=DELIVERY_TYPES)
    date = models.DateField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    workers = models.ManyToManyField(Worker)
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True)
    dock = models.ForeignKey(Dock, on_delete=models.SET_NULL, null=True)
    aisle = models.ForeignKey(Aisle, on_delete=models.SET_NULL, null=True)

STATUSES = {
    "in_warehouse": "In a warehouse",
    "on_truck": "On a truck",
    "unknown": "Unknown"
}

class Package(models.Model):
    serial_number = models.CharField(max_length=255)
    weight = models.IntegerField()
    size = models.IntegerField()
    status = models.CharField(
        max_length=255, 
        choices=STATUSES, 
        default="unknown"
    )
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True)
    payload_area = models.ForeignKey(PayloadArea, on_delete=models.SET_NULL, null=True)
    
    def validate_placement(self):
        if self.truck and self.payload_area:
           raise ValidationError("Package can't be in a truck and payload area at the same time!")
    
    def save(self, *args, **kwargs):
        self.validate_placement()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.serial_number}"
