from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from .forms import CompanyForm
from django.shortcuts import render, redirect
from .models import Company

@login_required
@permission_required('company.view_company', raise_exception=True)
def list_companies(request):
    # Filtruj firmy, które mają ustawione pole manager
    companies_with_manager = Company.objects.exclude(manager__isnull=True)
    p = Paginator(companies_with_manager, 3)
    page = request.GET.get('page')
    companies = p.get_page(page)
    return render(request, 'company/companies.html', {'companies': companies})

@login_required
@permission_required('company_add_company', raise_exception=True)
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-companies')
    else:
        form = CompanyForm()

    return render(request, 'company/add_company.html', {'form': form})

@login_required
@permission_required('company.view_company', raise_exception=True)
def show_company(request, company_id):
    company = Company.objects.get(pk=company_id)
    return render(request, 'company/show_company.html', {'company': company })
