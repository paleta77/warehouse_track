from django.urls import path
from . import views


urlpatterns = [
    path("companies/", views.companies, name="companies"),
    path("companies/<int:company_id>/", views.company_detail, name="company_detail"),
]
