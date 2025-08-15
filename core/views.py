# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Client, Document, Service, Task
from .forms import TaskForm
def index(request):
    return render(request, 'core/index.html')

def clients_list(request):
    clients = Client.objects.all()
    return render(request, 'core/clients_list.html', {'clients': clients})

def documents_list(request):
    documents = Document.objects.all()
    return render(request, 'core/documents_list.html', {'documents': documents})

def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('documents_list')
    else:
        form = DocumentForm()
    return render(request, 'core/add_document.html', {'form': form})

def edit_document(request, document_id):
    document = Document.objects.get(id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect('documents_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'core/edit_document.html', {'form': form})

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm()
    return render(request, 'core/add_client.html', {'form': form})

def edit_client(request, client_id):
    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'core/edit_client.html', {'form': form})

def services_list(request):
    from .forms import ServiceForm  # Import ServiceForm here
    services = Service.objects.all()
    return render(request, 'core/services_list.html', {'services': services})

def add_service(request):
    from .forms import ServiceForm  # Import ServiceForm inside the function
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services_list')
    else:
        form = ServiceForm()
    return render(request, 'core/add_service.html', {'form': form})

def edit_service(request, service_id):
    from .forms import ServiceForm  # Import ServiceForm inside the function
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'core/edit_service.html', {'form': form})
def tasks_list(request):
    tasks = Task.objects.all()
    return render(request, 'core/tasks_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks_list')
    else:
        form = TaskForm()
    return render(request, 'core/add_task.html', {'form': form})

def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'core/edit_task.html', {'form': form})
def tasks_list(request):
    tasks = Task.objects.all().order_by('due_date')

    # Get filter parameters from request
    status_filter = request.GET.get('status')
    assigned_to_filter = request.GET.get('assigned_to')

    # Apply filters if they are provided
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if assigned_to_filter:
        tasks = tasks.filter(assigned_to__username=assigned_to_filter)

    # Get a distinct list of users who are assigned to tasks
    assigned_users = User.objects.filter(task__isnull=False).distinct()

    # Pass filter parameters to the template
    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'assigned_to_filter': assigned_to_filter,
        'assigned_users': assigned_users,
    }
    return render(request, 'core/tasks_list.html', context)
def task_dashboard(request):
    # Count tasks by status
    total_tasks = Task.objects.count()
    not_started = Task.objects.filter(status='not_started').count()
    in_progress = Task.objects.filter(status='in_progress').count()
    completed = Task.objects.filter(status='completed').count()

    # Find tasks nearing due dates
    today = date.today()
    upcoming_tasks = Task.objects.filter(due_date__range=[today, today + timedelta(days=7)])

    context = {
        'total_tasks': total_tasks,
        'not_started': not_started,
        'in_progress': in_progress,
        'completed': completed,
        'upcoming_tasks': upcoming_tasks,
    }
    return render(request, 'core/task_dashboard.html', context)