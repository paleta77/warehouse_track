from django.contrib import admin
from .models import Company, Operator
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "telephone")


class OperatorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "company")


admin.site.register(Company, CompanyAdmin)
admin.site.register(Operator, OperatorAdmin)
