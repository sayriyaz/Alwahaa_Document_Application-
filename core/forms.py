from django import forms
from .models import Document, Client, Service, Task  # Import the Client model
# core/forms.py
from django import forms
from .models import Document, Client, Service, Task

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['client', 'title', 'description', 'submitted_date', 'status']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'address']

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'fee']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'client', 'assigned_to', 'status', 'due_date']
    
def services_list(request):
    services = Service.objects.all()
    return render(request, 'core/services_list.html', {'services': services})

def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services_list')
    else:
        form = ServiceForm()
    return render(request, 'core/add_service.html', {'form': form})

def edit_service(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'core/edit_service.html', {'form': form})
