from django.contrib import admin
from company.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    fields = (('companyName'), 'manager', 'zipCode', 'location', 'nip', 'businessArea')
    list_display = ('companyName', 'manager', 'zipCode', 'location', 'nip', 'businessArea')
    ordering = ('manager',)
    search_fields = ('companyName', 'manager', 'nip')
    filter = ('businessArea')
