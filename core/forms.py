# core/forms.py
from django import forms
from .models import Company, ServiceRequest, Task

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = "__all__"

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
