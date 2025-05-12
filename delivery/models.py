from django.db import models
from warehouse.models import PayloadArea, Dock, Aisle, Warehouse
from companies.models import Company
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.http import JsonResponse

# Create your models here.

class Truck(models.Model):
    registration_plates = models.CharField(max_length=15)
    brand = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.registration_plates} - {self.brand}"

class Driver(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = PhoneNumberField()
    email = models.EmailField(max_length=255)
    trucks = models.ManyToManyField(Truck)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Customer(models.Model):
    name = models.CharField(max_length=255)
    tax_number = models.CharField(max_length=255)
    telephone = PhoneNumberField()
    email = models.EmailField(max_length=255)
    
    def __str__(self):
        return f"{self.name}"
    
class Worker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    telephone = PhoneNumberField()
    email = models.EmailField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    work_start_hour = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        default=8
    )
    work_end_hour = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        default=16
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company}"
    
DELIVERY_TYPES = {
    "IN": "In",
    "OUT": "Out"
}
DELIVERY_STATUSES = {
    "at_dock": "At dock",
    "in_preparation": "In preparation",
    "ready_to_ship": "Ready to ship",
    "on_the_way": "On the way",
    "delivered": "Delivered",
    "cancelled": "Cancelled"
}

class Delivery(models.Model):
    
    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
    
    status = models.CharField(
        max_length=255, 
        choices=DELIVERY_STATUSES, 
        default="in_preparation"
    )
    delivery_number = models.CharField(max_length=255)
    delivery_type = models.CharField(max_length=255, choices=DELIVERY_TYPES)
    date = models.DateTimeField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    workers = models.ManyToManyField(Worker)
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True)
    dock = models.ForeignKey(Dock, on_delete=models.SET_NULL, null=True)
    aisle = models.ForeignKey(Aisle, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    packages = models.ManyToManyField("Package", blank=True)
    
    def __str__(self):
        return f"{self.delivery_number} - {self.customer}"
    
    def select_best_dock(self, packages=None):
        """
        Selects the dock with the shortest average Manhattan distance to the payload areas
        for all packages in this delivery, matching by payload_type.
        """
        if packages is None:
            packages = self.packages.all()
        docks = Dock.objects.filter(warehouse=self.warehouse)
        print("Docks:", list(docks))
        dock_distances = {}

        print("Packages:", list(packages))
        for package in packages:
            print("Payload areas for", package, ":", list(PayloadArea.objects.filter(
                aisle__warehouse=self.warehouse,
                payload_type=package.payload_type
            )))

        for dock in docks:
            total_distance = 0
            count = 0
            for package in packages:
                payload_areas = PayloadArea.objects.filter(
                    aisle__warehouse=self.warehouse,
                    payload_type=package.payload_type
                )
                min_distance = None
                for pa in payload_areas:
                    distance = abs(dock.number - pa.aisle.number) + abs(1 - pa.number)
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
                if min_distance is not None:
                    total_distance += min_distance
                    count += 1
            if count > 0:
                dock_distances[dock] = total_distance / count

        if dock_distances:
            best_dock = min(dock_distances, key=dock_distances.get)
            return best_dock
        return None

def get_best_dock(request):
    warehouse_id = request.GET.get("warehouse")
    package_ids = request.GET.getlist("packages[]")

    if warehouse_id and package_ids:
        customer = Customer.objects.first()
        temp_delivery = Delivery(warehouse_id=warehouse_id, customer=customer)
        packages_qs = Package.objects.filter(pk__in=package_ids)
        print("Docks:", list(Dock.objects.filter(warehouse=warehouse_id)))
        print("Packages:", list(packages_qs))
        for package in packages_qs:
            print("Payload areas for", package, ":", list(PayloadArea.objects.filter(
                aisle__warehouse=warehouse_id,
                payload_type=package.payload_type
            )))
        best_dock = temp_delivery.select_best_dock(packages=packages_qs)
        print("Best dock:", best_dock)
        return JsonResponse({"dock": best_dock.pk if best_dock else None})
    return JsonResponse({"dock": None})

STATUSES = {
    "in_warehouse": "In a warehouse",
    "on_truck": "On a truck",
    "unknown": "Unknown"
}

PAYLOAD_TYPES = {
    "food": "Food",
    "drinks": "Drinks",
    "rtv": "RTV",
    "agd": "AGD",
    "electronics": "Electronics",
    "other": "Other",
}

class Package(models.Model):
    serial_number = models.CharField(max_length=255)
    weight = models.IntegerField()
    size = models.IntegerField()
    payload_type = models.CharField(
        max_length=50, 
        choices=PAYLOAD_TYPES, 
        default="other"
    )
    status = models.CharField(
        max_length=255, 
        choices=STATUSES, 
        default="unknown"
    )
    truck = models.ForeignKey(Truck, on_delete=models.SET_NULL, null=True, blank=True)
    payload_area = models.ForeignKey(PayloadArea, on_delete=models.SET_NULL, null=True, blank=True)
    
    def validate_placement(self):
        if self.truck and self.payload_area:
           raise ValidationError("Package can't be in a truck and payload area at the same time!")
    
    def save(self, *args, **kwargs):
        self.validate_placement()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.serial_number}"
