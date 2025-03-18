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
