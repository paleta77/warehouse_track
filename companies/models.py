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
