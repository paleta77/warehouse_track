from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Company


@login_required(login_url="/")
def companies(request):
    companies = Company.objects.all()
    return render(request, "all_companies.html", {"companies": companies})


@login_required(login_url="/")
def company_detail(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    return render(request, "details_company.html", {"company": company})
