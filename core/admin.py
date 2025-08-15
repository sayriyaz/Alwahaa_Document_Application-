# core/admin.py
from django.contrib import admin
from .models import (
    Sponsor, Company, Owner, Employee, ServiceType, ServiceRequest,
    Visa, TradeLicense, EstablishmentCard, DocumentFile, Invoice, Payment,
    Task, TaskActivity
)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name","trade_license_number","trade_license_expiry","establishment_card_expiry","sponsor")
    search_fields = ("name","trade_license_number")
    list_filter = ("sponsor",)

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("company","service_type","status","created_at","submitted_at","completed_at")
    list_filter = ("status","service_type","company")
    search_fields = ("company__name",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title","service_request","assigned_to","status","due_date")
    list_filter = ("status","assigned_to")
    search_fields = ("title","service_request__company__name")

models_to_register = [
    Sponsor, Owner, Employee, ServiceType, Visa, TradeLicense,
    EstablishmentCard, DocumentFile, Invoice, Payment, TaskActivity
]
for m in models_to_register:
    try:
        admin.site.register(m)
    except admin.sites.AlreadyRegistered:
        pass
