from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    telephone = PhoneNumberField()
    address = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name}"

class Operator(models.Model):
    first_name = models.CharField(max_length=255)
    last_name =  models.CharField(max_length=255)
    telephone = PhoneNumberField()
    email = models.EmailField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company}"
    